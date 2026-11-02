from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from database.connection import execute_query
from graph.knowledge_graph import KnowledgeGraph

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'role', '') != 'admin':
            flash('Administrative privileges required to access this resource.', 'error')
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_careers = execute_query("SELECT COUNT(*) as cnt FROM careers", fetch='one')['cnt']
    total_skills = execute_query("SELECT COUNT(*) as cnt FROM skills", fetch='one')['cnt']
    total_students = execute_query("SELECT COUNT(*) as cnt FROM users WHERE role = 'student'", fetch='one')['cnt']
    total_recs = execute_query("SELECT COUNT(*) as cnt FROM recommendations", fetch='one')['cnt']

    recent_students = execute_query(
        """SELECT u.id, u.username, u.email, u.created_at, p.degree, p.branch, p.experience_level
           FROM users u
           LEFT JOIN student_profiles p ON u.id = p.user_id
           WHERE u.role = 'student'
           ORDER BY u.created_at DESC LIMIT 5""",
        fetch='all'
    ) or []

    recent_recs = execute_query(
        """SELECT r.*, u.username, c.title as career_title
           FROM recommendations r
           JOIN users u ON r.user_id = u.id
           JOIN careers c ON r.career_id = c.id
           ORDER BY r.created_at DESC LIMIT 5""",
        fetch='all'
    ) or []

    return render_template(
        'admin/dashboard.html',
        total_careers=total_careers,
        total_skills=total_skills,
        total_students=total_students,
        total_recs=total_recs,
        recent_students=recent_students,
        recent_recs=recent_recs
    )

@admin_bp.route('/careers')
@admin_required
def careers():
    all_careers = execute_query("SELECT * FROM careers ORDER BY id ASC", fetch='all') or []
    # Count mapped skills for each
    for c in all_careers:
        cnt_res = execute_query(
            "SELECT COUNT(*) as cnt FROM career_skills WHERE career_id = %s",
            (c['id'],),
            fetch='one'
        )
        c['skills_count'] = cnt_res['cnt'] if cnt_res else 0

    return render_template('admin/careers.html', careers=all_careers)

@admin_bp.route('/careers/add', methods=['POST'])
@admin_required
def add_career():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'General').strip()
    description = request.form.get('description', '').strip()
    salary = request.form.get('average_salary', '$85,000').strip()
    outlook = request.form.get('job_outlook', 'High Demand').strip()

    if not title:
        flash('Career title is required.', 'error')
        return redirect(url_for('admin.careers'))

    execute_query(
        """INSERT INTO careers (title, category, description, average_salary, job_outlook)
           VALUES (%s, %s, %s, %s, %s)""",
        (title, category, description, salary, outlook),
        commit=True
    )
    # Refresh graph
    KnowledgeGraph._instance = None
    flash(f'Career "{title}" successfully added!', 'success')
    return redirect(url_for('admin.careers'))

@admin_bp.route('/careers/edit/<int:career_id>', methods=['POST'])
@admin_required
def edit_career(career_id):
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    salary = request.form.get('average_salary', '').strip()
    outlook = request.form.get('job_outlook', '').strip()

    execute_query(
        """UPDATE careers 
           SET title = %s, category = %s, description = %s, average_salary = %s, job_outlook = %s
           WHERE id = %s""",
        (title, category, description, salary, outlook, career_id),
        commit=True
    )
    KnowledgeGraph._instance = None
    flash('Career profile updated successfully.', 'success')
    return redirect(url_for('admin.careers'))

@admin_bp.route('/careers/delete/<int:career_id>', methods=['POST'])
@admin_required
def delete_career(career_id):
    execute_query("DELETE FROM careers WHERE id = %s", (career_id,), commit=True)
    KnowledgeGraph._instance = None
    flash('Career entity removed from database and ontology.', 'info')
    return redirect(url_for('admin.careers'))

@admin_bp.route('/skills')
@admin_required
def skills():
    all_skills = execute_query("SELECT * FROM skills ORDER BY category, name", fetch='all') or []
    return render_template('admin/skills.html', skills=all_skills)

@admin_bp.route('/skills/add', methods=['POST'])
@admin_required
def add_skill():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', 'General').strip()
    difficulty = request.form.get('difficulty_level', 'Beginner').strip()

    if not name:
        flash('Skill name is required.', 'error')
        return redirect(url_for('admin.skills'))

    execute_query(
        "INSERT INTO skills (name, category, difficulty_level) VALUES (%s, %s, %s)",
        (name, category, difficulty),
        commit=True
    )
    KnowledgeGraph._instance = None
    flash(f'Skill "{name}" added to ontology.', 'success')
    return redirect(url_for('admin.skills'))

@admin_bp.route('/skills/edit/<int:skill_id>', methods=['POST'])
@admin_required
def edit_skill(skill_id):
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    difficulty = request.form.get('difficulty_level', '').strip()

    execute_query(
        "UPDATE skills SET name = %s, category = %s, difficulty_level = %s WHERE id = %s",
        (name, category, difficulty, skill_id),
        commit=True
    )
    KnowledgeGraph._instance = None
    flash('Skill entity updated successfully.', 'success')
    return redirect(url_for('admin.skills'))

@admin_bp.route('/skills/delete/<int:skill_id>', methods=['POST'])
@admin_required
def delete_skill(skill_id):
    execute_query("DELETE FROM skills WHERE id = %s", (skill_id,), commit=True)
    KnowledgeGraph._instance = None
    flash('Skill entity deleted.', 'info')
    return redirect(url_for('admin.skills'))

@admin_bp.route('/relationships')
@admin_required
def relationships():
    career_id = request.args.get('career_id', type=int)
    if career_id:
        links = execute_query(
            """SELECT cs.id, cs.career_id, cs.skill_id, cs.importance, cs.skill_type,
                      c.title as career_title, s.name as skill_name, s.category as skill_category
               FROM career_skills cs
               JOIN careers c ON cs.career_id = c.id
               JOIN skills s ON cs.skill_id = s.id
               WHERE cs.career_id = %s
               ORDER BY cs.importance DESC""",
            (career_id,),
            fetch='all'
        ) or []
    else:
        links = execute_query(
            """SELECT cs.id, cs.career_id, cs.skill_id, cs.importance, cs.skill_type,
                      c.title as career_title, s.name as skill_name, s.category as skill_category
               FROM career_skills cs
               JOIN careers c ON cs.career_id = c.id
               JOIN skills s ON cs.skill_id = s.id
               ORDER BY cs.id DESC LIMIT 100""",
            fetch='all'
        ) or []

    careers_list = execute_query("SELECT id, title FROM careers ORDER BY title", fetch='all') or []
    skills_list = execute_query("SELECT id, name FROM skills ORDER BY name", fetch='all') or []

    return render_template(
        'admin/relationships.html',
        links=links,
        careers=careers_list,
        skills=skills_list,
        selected_career_id=career_id
    )

@admin_bp.route('/relationships/add', methods=['POST'])
@admin_required
def add_relationship():
    career_id = request.form.get('career_id', type=int)
    skill_id = request.form.get('skill_id', type=int)
    importance = float(request.form.get('importance', 0.8))
    skill_type = request.form.get('skill_type', 'Required')

    if career_id and skill_id:
        execute_query(
            """INSERT INTO career_skills (career_id, skill_id, importance, skill_type)
               VALUES (%s, %s, %s, %s)""",
            (career_id, skill_id, importance, skill_type),
            commit=True
        )
        KnowledgeGraph._instance = None
        flash('Career-Skill requirement edge linked successfully!', 'success')
    return redirect(url_for('admin.relationships', career_id=career_id))

@admin_bp.route('/relationships/delete/<int:rel_id>', methods=['POST'])
@admin_required
def delete_relationship(rel_id):
    career_id = request.form.get('career_id', type=int)
    execute_query("DELETE FROM career_skills WHERE id = %s", (rel_id,), commit=True)
    KnowledgeGraph._instance = None
    flash('Relationship edge disconnected.', 'info')
    return redirect(url_for('admin.relationships', career_id=career_id))

@admin_bp.route('/students')
@admin_required
def students():
    students_list = execute_query(
        """SELECT u.id, u.username, u.email, u.created_at,
                  p.full_name, p.degree, p.branch, p.graduation_year, p.experience_level,
                  c.title as target_career
           FROM users u
           LEFT JOIN student_profiles p ON u.id = p.user_id
           LEFT JOIN careers c ON p.target_career_id = c.id
           WHERE u.role = 'student'
           ORDER BY u.created_at DESC""",
        fetch='all'
    ) or []

    for st in students_list:
        sk_cnt = execute_query("SELECT COUNT(*) as cnt FROM student_skills WHERE user_id = %s", (st['id'],), fetch='one')
        st['skills_count'] = sk_cnt['cnt'] if sk_cnt else 0

    return render_template('admin/students.html', students=students_list)

@admin_bp.route('/recommendations-log')
@admin_required
def recommendations_log():
    logs = execute_query(
        """SELECT r.*, u.username, u.email, c.title as career_title, c.category
           FROM recommendations r
           JOIN users u ON r.user_id = u.id
           JOIN careers c ON r.career_id = c.id
           ORDER BY r.created_at DESC LIMIT 100""",
        fetch='all'
    ) or []
    return render_template('admin/recommendations_log.html', logs=logs)

@admin_bp.route('/statistics')
@admin_required
def statistics():
    kg_instance = KnowledgeGraph.get_instance()
    stats = kg_instance.get_stats()
    return render_template('admin/statistics.html', stats=stats)

