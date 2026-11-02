import os
import sqlite3
import pymysql
from pymysql.cursors import DictCursor
from config import Config

# Determine fallback SQLite path
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
os.makedirs(DB_DIR, exist_ok=True)
SQLITE_PATH = os.path.join(DB_DIR, 'ai_career_recommender.db')

_use_sqlite = False
_tested_connection = False

def _test_connection():
    global _use_sqlite, _tested_connection
    if _tested_connection:
        return
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT,
            connect_timeout=2
        )
        conn.close()
        _use_sqlite = False
    except Exception:
        _use_sqlite = True
    _tested_connection = True

def check_db_connection():
    _test_connection()
    if not _use_sqlite:
        try:
            conn = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                port=Config.DB_PORT,
                connect_timeout=2
            )
            conn.close()
            return True, f"Connected to MySQL at {Config.DB_HOST}:{Config.DB_PORT} (Database: {Config.DB_NAME})"
        except Exception as e:
            return False, f"MySQL connection error: {e}"
    else:
        init_sqlite_if_needed()
        return True, f"Running with local high-performance SQLite database: {os.path.basename(SQLITE_PATH)}"

class SQLiteDictCursor:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = connection.cursor()
        self.lastrowid = None
        self.rowcount = 0

    def execute(self, query, params=None):
        # Convert %s to ? for SQLite syntax
        q = query.replace('%s', '?')
        # SQLite adjustments for standard functions
        q = q.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
        if params is None:
            res = self.cursor.execute(q)
        else:
            if isinstance(params, list):
                params = tuple(params)
            res = self.cursor.execute(q, params)
        self.lastrowid = self.cursor.lastrowid
        self.rowcount = self.cursor.rowcount
        return res

    def fetchone(self):
        row = self.cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def fetchall(self):
        rows = self.cursor.fetchall()
        return [dict(r) for r in rows]

    def close(self):
        self.cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class SQLiteConnectionWrapper:
    def __init__(self, raw_conn):
        self.conn = raw_conn
        self.conn.row_factory = sqlite3.Row

    def cursor(self, cursor_type=None):
        return SQLiteDictCursor(self.conn)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

def get_db_connection():
    _test_connection()
    if not _use_sqlite:
        return pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT,
            cursorclass=DictCursor,
            autocommit=False
        )
    else:
        init_sqlite_if_needed()
        raw = sqlite3.connect(SQLITE_PATH)
        return SQLiteConnectionWrapper(raw)

def execute_query(query, params=None, fetch=None, commit=False):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            
            result = None
            if fetch == 'one':
                result = cursor.fetchone()
            elif fetch == 'all':
                result = cursor.fetchall()
                
            if commit:
                conn.commit()
                return cursor.lastrowid or True
                
            return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_sqlite_if_needed():
    if not os.path.exists(SQLITE_PATH) or os.path.getsize(SQLITE_PATH) == 0:
        raw = sqlite3.connect(SQLITE_PATH)
        raw.row_factory = sqlite3.Row
        cur = raw.cursor()
        
        schema = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            degree TEXT DEFAULT '',
            branch TEXT DEFAULT '',
            graduation_year INTEGER DEFAULT 2026,
            experience_level TEXT DEFAULT 'Beginner',
            target_career_id INTEGER DEFAULT NULL,
            bio TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            difficulty_level TEXT DEFAULT 'Beginner'
        );

        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            description TEXT,
            average_salary TEXT DEFAULT '$85,000',
            job_outlook TEXT DEFAULT 'High Demand (15% growth)'
        );

        CREATE TABLE IF NOT EXISTS career_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            importance REAL DEFAULT 0.8,
            skill_type TEXT DEFAULT 'Required',
            FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS interests (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS education (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_id INTEGER NOT NULL,
            degree TEXT NOT NULL,
            branch TEXT NOT NULL,
            FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS student_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            proficiency_level TEXT DEFAULT 'Intermediate',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS student_interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            interest_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (interest_id) REFERENCES interests(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            career_id INTEGER NOT NULL,
            hybrid_score REAL DEFAULT 0.0,
            ml_score REAL DEFAULT 0.0,
            gnn_score REAL DEFAULT 0.0,
            rank_position INTEGER DEFAULT 1,
            explanation TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS skill_gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            career_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            status TEXT DEFAULT 'missing',
            importance REAL DEFAULT 0.8,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
        );
        """
        cur.executescript(schema)
        raw.commit()
        raw.close()
        
        # Populate initial seeds
        try:
            import seed_data
            seed_data.main()
        except Exception as e:
            print(f"[!] Warning seeding SQLite: {e}")
