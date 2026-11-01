import os
import csv
from database.connection import execute_query

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def clear_existing_data():
    """
    Clear all records from database tables to prevent duplicate key errors during seeding.
    """
    print("[*] Clearing existing database tables...")
    from database.connection import get_db_connection
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            tables = [
                "student_skills", "student_interests", "career_skills", 
                "education", "skill_gaps", "recommendations", 
                "skills", "careers", "interests", "student_profiles", "users"
            ]
            for t in tables:
                cursor.execute(f"TRUNCATE TABLE {t};")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        connection.commit()
        print("[+] Database cleared successfully.")
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def seed_skills():
    print("[*] Seeding skills table...")
    skills_path = os.path.join(DATA_DIR, 'skills.csv')
    
    count = 0
    with open(skills_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            difficulty = row.get('difficulty_level', 'Beginner') or 'Beginner'
            execute_query(
                "INSERT INTO skills (id, name, category, difficulty_level) VALUES (%s, %s, %s, %s)",
                (int(row['id']), row['name'], row['category'], difficulty),
                commit=True
            )
            count += 1
    print(f"[+] Seeded {count} skills.")

def seed_careers():
    print("[*] Seeding careers table...")
    careers_path = os.path.join(DATA_DIR, 'careers.csv')
    job_market_path = os.path.join(DATA_DIR, 'job_market.csv')
    
    # Load job market details into dictionary indexed by career_id
    job_market = {}
    with open(job_market_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_market[int(row['career_id'])] = row
            
    count = 0
    with open(careers_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c_id = int(row['id'])
            jm = job_market.get(c_id, {})
            
            # Map salary and outlook from job market
            avg_salary = jm.get('avg_salary', '75000')
            demand = jm.get('demand_score', 'Medium')
            growth = jm.get('growth_rate_pct', '10.0')
            
            job_outlook = f"{demand} Demand ({growth}% growth)"
            
            execute_query(
                "INSERT INTO careers (id, title, category, description, average_salary, job_outlook) VALUES (%s, %s, %s, %s, %s, %s)",
                (c_id, row['title'], row.get('category', 'General'), row['description'], f"${avg_salary}", job_outlook),
                commit=True
            )
            count += 1
            
            # Add dynamic education requirements mapping
            # (AI/ML requires CS or Data Science; Software Eng requires CS/IT/BCA/MCA; Business requires MBA)
            category = row['category']
            if category == 'AI/ML':
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Data Science')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Computer Science')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'M.Sc', 'Computer Science')", (c_id,), commit=True)
            elif category == 'Software Engineering':
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Computer Science')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Information Technology')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'BCA', 'Computer Science')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'MCA', 'Computer Science')", (c_id,), commit=True)
            elif category == 'Business & Product':
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'MBA', 'Business Administration')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Computer Science')", (c_id,), commit=True)
            elif category == 'Robotics & Hardware':
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Electronics')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Computer Science')", (c_id,), commit=True)
            else: # general tech careers accept CS/IT
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Computer Science')", (c_id,), commit=True)
                execute_query("INSERT INTO education (career_id, degree, branch) VALUES (%s, 'B.Tech', 'Information Technology')", (c_id,), commit=True)

    print(f"[+] Seeded {count} careers and mapped educational guidelines.")

def seed_interests():
    print("[*] Seeding interests table...")
    interests_path = os.path.join(DATA_DIR, 'interests.csv')
    
    count = 0
    with open(interests_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            execute_query(
                "INSERT INTO interests (id, name) VALUES (%s, %s)",
                (int(row['id']), row['name']),
                commit=True
            )
            count += 1
    print(f"[+] Seeded {count} interests.")

def seed_career_skills():
    print("[*] Seeding career-skills relationships...")
    cs_path = os.path.join(DATA_DIR, 'career_skills.csv')
    
    count = 0
    with open(cs_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            skill_type = row.get('skill_type', 'Required') or 'Required'
            execute_query(
                "INSERT INTO career_skills (career_id, skill_id, importance, skill_type) VALUES (%s, %s, %s, %s)",
                (int(row['career_id']), int(row['skill_id']), float(row['importance']), skill_type),
                commit=True
            )
            count += 1
    print(f"[+] Seeded {count} career-skill links.")

def create_admin_user():
    print("[*] Creating baseline users...")
    from werkzeug.security import generate_password_hash
    
    # 1. Create standard Admin User
    admin_pass = generate_password_hash('admin123')
    admin_id = execute_query(
        "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        ('admin', 'admin@edupath.ai', admin_pass, 'admin'),
        commit=True
    )
    print(f"[+] Created Administrator Account (username: admin, password: admin123)")

    # 2. Create demo Student User
    student_pass = generate_password_hash('student123')
    student_id = execute_query(
        "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        ('demostudent', 'student@edupath.ai', student_pass, 'student'),
        commit=True
    )
    
    # Initialize profile for student
    execute_query(
        """INSERT INTO student_profiles (user_id, full_name, phone, degree, branch, graduation_year, experience_level) 
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (student_id, 'Jane Doe', '9876543210', 'B.Tech', 'Computer Science', 2026, 'Beginner'),
        commit=True
    )
    print(f"[+] Created Demo Student Account (username: demostudent, password: student123)")

def main():
    print("==========================================")
    print(" EduPath AI - Database Seeding Procedure ")
    print("==========================================\n")
    
    # Verify CSV files exist
    if not os.path.exists(os.path.join(DATA_DIR, 'skills.csv')):
        print("[Error] CSV files not found. Please verify data/skills.csv exists.")
        return
        
    try:
        clear_existing_data()
        seed_skills()
        seed_careers()
        seed_interests()
        seed_career_skills()
        create_admin_user()
        print("\n==========================================")
        print("[SUCCESS] Database seeding completed successfully!")
        print("==========================================")
    except Exception as e:
        print(f"\n[Error] Database seeding failed: {e}")

if __name__ == '__main__':
    main()
