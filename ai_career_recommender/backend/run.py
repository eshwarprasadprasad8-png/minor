import os
import sys

# Ensure backend directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from database.connection import check_db_connection

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("  AI-Based Skill & Career Recommendation System")
    print("  Hybrid ML + PyG GraphSAGE Architecture")
    print("=" * 60)

    # Check database status
    connected, message = check_db_connection()
    if connected:
        print(f"[*] Database: {message}")
    else:
        print(f"[!] Database warning: {message}")

    print("\n[*] Demo Credentials:")
    print("    - Admin:   username 'admin',       password 'admin123'")
    print("    - Student: username 'demostudent', password 'student123'")
    print("\n[*] Server starting on http://127.0.0.1:5000 ...")
    print("=" * 60)

    app.run(host='127.0.0.1', port=5000, debug=True)

