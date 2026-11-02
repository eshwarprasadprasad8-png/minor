from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from database.connection import execute_query

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    # 1. Fetch Student Profile
    profile = execute_query(
        """SELECT p.*, c.title as target_career_title, c.category as target_career_category
           FROM student_profiles p
           LEFT JOIN careers c ON p.target_career_id = c.id
           WHERE p.user_id = %s""",
        (current_user.id,),
        fetch='one'
    ) or {}

    # 2. Counts
    skills_count_res = execute_query(
        "SELECT COUNT(*) as cnt FROM student_skills WHERE user_id = %s",
        (current_user.id,),
        fetch='one'
    )
    skills_count = skills_count_res['cnt'] if skills_count_res else 0

    interests_count_res = execute_query(
        "SELECT COUNT(*) as cnt FROM student_interests WHERE user_id = %s",
        (current_user.id,),
        fetch='one'
    )
    interests_count = interests_count_res['cnt'] if interests_count_res else 0

    # 3. Top recommendations preview
    top_recommendations = execute_query(
        """SELECT r.*, c.title, c.category, c.average_salary, c.job_outlook, c.description
           FROM recommendations r
           JOIN careers c ON r.career_id = c.id
           WHERE r.user_id = %s
           ORDER BY r.rank_position ASC
           LIMIT 4""",
        (current_user.id,),
        fetch='all'
    ) or []

    # If no recommendations yet, pull top 4 based on student skills or default
    if not top_recommendations:
        careers = execute_query("SELECT id, title, category, average_salary, job_outlook, description FROM careers LIMIT 4", fetch='all') or []
        top_recommendations = [
            {
                'career_id': c['id'],
                'title': c['title'],
                'category': c['category'],
                'average_salary': c['average_salary'],
                'job_outlook': c['job_outlook'],
                'description': c['description'],
                'hybrid_score': 0.88 - (idx * 0.06),
                'rank_position': idx + 1
            }
            for idx, c in enumerate(careers)
        ]

    # 4. Verified student skills list
    student_skills = execute_query(
        """SELECT s.id, s.name, s.category, s.difficulty_level, ss.proficiency_level
           FROM student_skills ss
           JOIN skills s ON ss.skill_id = s.id
           WHERE ss.user_id = %s
           ORDER BY s.category, s.name""",
        (current_user.id,),
        fetch='all'
    ) or []

    # 5. Profile Completion Percentage
    completion = 20
    if profile.get('full_name') and profile.get('degree'):
        completion += 20
    if interests_count > 0:
        completion += 20
    if skills_count > 0:
        completion += 20
    if profile.get('target_career_id'):
        completion += 20

    return render_template(
        'dashboard.html',
        profile=profile,
        skills_count=skills_count,
        interests_count=interests_count,
        top_recommendations=top_recommendations,
        student_skills=student_skills,
        completion=completion
    )

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        degree = request.form.get('degree', '').strip()
        branch = request.form.get('branch', '').strip()
        grad_year = request.form.get('graduation_year', 2026)
        experience = request.form.get('experience_level', 'Beginner')
        bio = request.form.get('bio', '').strip()

        execute_query(
            """UPDATE student_profiles 
               SET full_name = %s, phone = %s, degree = %s, branch = %s, graduation_year = %s, experience_level = %s, bio = %s
               WHERE user_id = %s""",
            (full_name, phone, degree, branch, grad_year, experience, bio, current_user.id),
            commit=True
        )
        flash('Profile details updated successfully!', 'success')
        return redirect(url_for('student.profile'))

    profile_data = execute_query(
        "SELECT * FROM student_profiles WHERE user_id = %s",
        (current_user.id,),
        fetch='one'
    ) or {}

    return render_template('profile.html', profile=profile_data)

@student_bp.route('/education', methods=['GET', 'POST'])
@login_required
def education():
    if request.method == 'POST':
        degree = request.form.get('degree', '').strip()
        branch = request.form.get('branch', '').strip()
        graduation_year = request.form.get('graduation_year', 2026)

        execute_query(
            "UPDATE student_profiles SET degree = %s, branch = %s, graduation_year = %s WHERE user_id = %s",
            (degree, branch, graduation_year, current_user.id),
            commit=True
        )
        flash('Education details saved!', 'success')
        return redirect(url_for('student.interests'))

    profile_data = execute_query(
        "SELECT degree, branch, graduation_year FROM student_profiles WHERE user_id = %s",
        (current_user.id,),
        fetch='one'
    ) or {}

    return render_template('education.html', profile=profile_data)

@student_bp.route('/interests', methods=['GET', 'POST'])
@login_required
def interests():
    if request.method == 'POST':
        selected_interests = request.form.getlist('interests')
        # Clear existing
        execute_query("DELETE FROM student_interests WHERE user_id = %s", (current_user.id,), commit=True)
        # Re-insert
        for i_id in selected_interests:
            execute_query(
                "INSERT INTO student_interests (user_id, interest_id) VALUES (%s, %s)",
                (current_user.id, int(i_id)),
                commit=True
            )
        flash('Career domain interests updated!', 'success')
        return redirect(url_for('student.skills'))

    all_interests = execute_query("SELECT id, name FROM interests ORDER BY id", fetch='all') or []
    user_interests = execute_query(
        "SELECT interest_id FROM student_interests WHERE user_id = %s",
        (current_user.id,),
        fetch='all'
    ) or []
    selected_ids = [row['interest_id'] for row in user_interests]

    return render_template('interests.html', interests=all_interests, selected_ids=selected_ids)

@student_bp.route('/skills', methods=['GET', 'POST'])
@login_required
def skills():
    if request.method == 'POST':
        selected_skills = request.form.getlist('skills')
        execute_query("DELETE FROM student_skills WHERE user_id = %s", (current_user.id,), commit=True)
        for s_id in selected_skills:
            execute_query(
                "INSERT INTO student_skills (user_id, skill_id, proficiency_level) VALUES (%s, %s, %s)",
                (current_user.id, int(s_id), 'Intermediate'),
                commit=True
            )
        flash('Skills catalog updated successfully!', 'success')
        return redirect(url_for('student.preferences'))

    all_skills = execute_query(
        "SELECT id, name, category, difficulty_level FROM skills ORDER BY category, name",
        fetch='all'
    ) or []
    user_skills = execute_query(
        "SELECT skill_id FROM student_skills WHERE user_id = %s",
        (current_user.id,),
        fetch='all'
    ) or []
    selected_ids = [row['skill_id'] for row in user_skills]

    return render_template('skills.html', skills=all_skills, selected_ids=selected_ids)

@student_bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'POST':
        target_career_id = request.form.get('target_career_id')
        if target_career_id:
            execute_query(
                "UPDATE student_profiles SET target_career_id = %s WHERE user_id = %s",
                (int(target_career_id), current_user.id),
                commit=True
            )
        flash('Target career preference updated!', 'success')
        return redirect(url_for('recommendations.get_recommendations'))

    careers = execute_query("SELECT id, title, category, description, average_salary FROM careers ORDER BY title", fetch='all') or []
    profile_data = execute_query("SELECT target_career_id FROM student_profiles WHERE user_id = %s", (current_user.id,), fetch='one') or {}
    selected_career_id = profile_data.get('target_career_id')

    return render_template('preferences.html', careers=careers, selected_career_id=selected_career_id)
