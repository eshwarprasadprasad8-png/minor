#!/usr/bin/env python
"""
Automated Database Initialization and Seeding Script
Executes schema.sql and runs seed_data.py to prepare MySQL for the AI Career Recommender.
"""
import os
import sys
import pymysql
from config import Config
import seed_data

def execute_sql_file(connection, sql_filepath):
    print(f"[*] Reading and executing SQL script: {os.path.basename(sql_filepath)}...")
    with open(sql_filepath, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split by semicolon while ignoring comments
    statements = sql_content.split(';')
    with connection.cursor() as cursor:
        for statement in statements:
            stmt = statement.strip()
            if stmt:
                # Avoid executing purely comment lines
                lines = [line for line in stmt.splitlines() if not line.strip().startswith('--')]
                cleaned_stmt = "\n".join(lines).strip()
                if cleaned_stmt:
                    cursor.execute(cleaned_stmt)
    connection.commit()
    print("[+] Schema creation completed successfully.")

def init_database():
    print("=" * 60)
    print("  AI CAREER RECOMMENDER - DATABASE INITIALIZATION")
    print("=" * 60)
    print(f"[*] Connecting to MySQL Server at {Config.DB_HOST}:{Config.DB_PORT} as '{Config.DB_USER}'...")

    try:
        # Connect to MySQL server without specifying a database first
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            autocommit=True
        )
        print("[+] MySQL server connection established.")
    except Exception as e:
        print(f"\n[!] Failed to connect to MySQL server: {e}")
        print("[!] Please verify MySQL is running (e.g. XAMPP, MySQL Service) and check backend/.env credentials.")
        sys.exit(1)

    try:
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
        if not os.path.exists(schema_path):
            print(f"[!] Error: {schema_path} not found.")
            sys.exit(1)

        execute_sql_file(conn, schema_path)
    except Exception as e:
        print(f"[!] Error executing schema: {e}")
        sys.exit(1)
    finally:
        conn.close()

    # Now run seed data
    print("\n[*] Populating initial database records and demo accounts...")
    try:
        seed_data.main()
        print("\n" + "=" * 60)
        print("[SUCCESS] Database initialization and seeding complete!")
        print("  - Admin:   username 'admin',       password 'admin123'")
        print("  - Student: username 'demostudent', password 'student123'")
        print("=" * 60)
    except Exception as e:
        print(f"[!] Seeding error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    init_database()
