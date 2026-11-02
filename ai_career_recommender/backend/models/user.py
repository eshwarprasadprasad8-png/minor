from flask_login import UserMixin
from database.connection import execute_query

class User(UserMixin):
    def __init__(self, id, username, email, role='student'):
        self.id = int(id)
        self.username = username
        self.email = email
        self.role = role

    def get_id(self):
        return str(self.id)

    @classmethod
    def get(cls, user_id):
        try:
            row = execute_query(
                "SELECT id, username, email, role FROM users WHERE id = %s",
                (user_id,),
                fetch='one'
            )
            if row:
                return cls(row['id'], row['username'], row['email'], row.get('role', 'student'))
        except Exception as e:
            print(f"[!] Error fetching user {user_id}: {e}")
        return None

    @classmethod
    def get_by_username(cls, username):
        try:
            row = execute_query(
                "SELECT id, username, email, password_hash, role FROM users WHERE username = %s OR email = %s",
                (username, username),
                fetch='one'
            )
            if row:
                user = cls(row['id'], row['username'], row['email'], row.get('role', 'student'))
                return user, row['password_hash']
        except Exception as e:
            print(f"[!] Error fetching user by username {username}: {e}")
        return None, None
