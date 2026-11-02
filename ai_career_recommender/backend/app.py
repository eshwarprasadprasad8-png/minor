import os
from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, current_user
from config import Config

def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.abspath(os.path.join(base_dir, '..', 'frontend', 'templates'))
    static_dir = os.path.abspath(os.path.join(base_dir, '..', 'frontend', 'static'))

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )
    app.config.from_object(Config)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    # Register User Loader for Flask-Login
    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.recommendations import recommendations_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(admin_bp)

    # Root Home Route
    @app.route('/')
    def home():
        from database.connection import execute_query
        try:
            featured_careers = execute_query(
                "SELECT id, title, category, average_salary, job_outlook, description FROM careers LIMIT 6",
                fetch='all'
            ) or []
            skills_cnt = execute_query("SELECT COUNT(*) as cnt FROM skills", fetch='one')
            total_skills = skills_cnt['cnt'] if skills_cnt else 102
            careers_cnt = execute_query("SELECT COUNT(*) as cnt FROM careers", fetch='one')
            total_careers = careers_cnt['cnt'] if careers_cnt else 40
        except Exception:
            featured_careers = []
            total_skills = 102
            total_careers = 40

        return render_template(
            'index.html',
            featured_careers=featured_careers,
            total_skills=total_skills,
            total_careers=total_careers
        )

    return app

if __name__ == '__main__':
    app = create_app()
    # Check database connection status on startup
    from database.connection import check_db_connection
    connected, message = check_db_connection()
    if connected:
        print(f"[*] Database check: {message}")
    else:
        print(f"[!] Database warning: {message}")
        print("[!] Make sure to run MySQL server and create database 'ai_career_recommender'.")
        
    print("[*] Starting AI-Based Skill & Career Recommendation System...")
    app.run(host='127.0.0.1', port=5000, debug=True)
