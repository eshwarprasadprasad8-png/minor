from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import execute_query
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user, password_hash = User.get_by_username(username)
        
        if user and check_password_hash(password_hash, password):
            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'student')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if confirm_password and password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
            
        try:
            # Check if username or email already exists
            existing_user = execute_query(
                "SELECT id FROM users WHERE username = %s OR email = %s",
                (username, email),
                fetch='one'
            )
            if existing_user:
                flash('Username or email already registered.', 'error')
                return render_template('register.html')
                
            # Create user
            password_hash = generate_password_hash(password)
            user_id = execute_query(
                "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (username, email, password_hash, role),
                commit=True
            )
            
            # Pre-create blank profile for students
            if role == 'student':
                execute_query(
                    "INSERT INTO student_profiles (user_id, full_name, degree, branch, graduation_year) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, username, '', '', 2026),
                    commit=True
                )
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'An error occurred during registration: {e}', 'error')
            
    return render_template('register.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
        
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not identifier or not new_password or not confirm_password:
            flash('All fields are required.', 'error')
            return render_template('forgot_password.html')
            
        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('forgot_password.html')
            
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('forgot_password.html')
            
        try:
            # Look up account by username or email
            user_data = execute_query(
                "SELECT id, username, email FROM users WHERE username = %s OR email = %s",
                (identifier, identifier),
                fetch='one'
            )
            
            if not user_data:
                flash('No account found with that username or email address.', 'error')
                return render_template('forgot_password.html')
                
            # Update password
            new_hash = generate_password_hash(new_password)
            execute_query(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (new_hash, user_data['id']),
                commit=True
            )
            
            flash(f'Password for account "{user_data["username"]}" has been successfully reset! Please sign in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'An error occurred while resetting your password: {e}', 'error')
            
    return render_template('forgot_password.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
