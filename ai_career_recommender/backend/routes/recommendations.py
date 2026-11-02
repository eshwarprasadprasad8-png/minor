from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from database.connection import execute_query
from services.recommendation_engine import RecommendationEngine
from services.alternative_careers import AlternativeCareersEngine
from services.explainer import ExplainerService
from services.learning_path import LearningPathEngine
from graph.knowledge_graph import KnowledgeGraph

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/recommendations')

rec_engine = RecommendationEngine()
alt_engine = AlternativeCareersEngine()
explainer_service = ExplainerService()
path_engine = LearningPathEngine()
kg = KnowledgeGraph.get_instance()

def _get_student_base_career_id():
    """Helper to determine student's primary career of focus."""
    # 1. Target career in profile
    profile = execute_query(
        "SELECT target_career_id FROM student_profiles WHERE user_id = %s",
        (current_user.id,),
        fetch='one'
    )
    if profile and profile.get('target_career_id'):
        return profile['target_career_id']

    # 2. Top-1 recommended career
    top_rec = execute_query(
        "SELECT career_id FROM recommendations WHERE user_id = %s ORDER BY rank_position ASC LIMIT 1",
        (current_user.id,),
        fetch='one'
    )
    if top_rec:
        return top_rec['career_id']

    # 3. Default to career 1
    c1 = execute_query("SELECT id FROM careers ORDER BY id ASC LIMIT 1", fetch='one')
    return c1['id'] if c1 else 1

def _get_recommended_career_options():
    recs = execute_query(
        """SELECT r.career_id as id, c.title, r.hybrid_score as score
           FROM recommendations r
           JOIN careers c ON r.career_id = c.id
           WHERE r.user_id = %s
           ORDER BY r.rank_position ASC""",
        (current_user.id,),
        fetch='all'
    )
    if not recs:
        # Fallback to top 5 careers
        careers = execute_query("SELECT id, title FROM careers LIMIT 5", fetch='all') or []
        recs = [{'id': c['id'], 'title': c['title'], 'score': 0.85 - (idx * 0.05)} for idx, c in enumerate(careers)]
    return recs

@recommendations_bp.route('/')
@login_required
def get_recommendations():
    refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    # Check if recommendations exist
    existing = execute_query(
        """SELECT r.*, c.title, c.category, c.average_salary, c.job_outlook, c.description
           FROM recommendations r
           JOIN careers c ON r.career_id = c.id
           WHERE r.user_id = %s
           ORDER BY r.rank_position ASC""",
        (current_user.id,),
        fetch='all'
    )

    if not existing or refresh:
        results = rec_engine.generate_recommendations(current_user.id, persist=True)
    else:
        results = existing
        # Format fields for template display
        for r in results:
            career_skills = kg.get_career_skills(r['career_id'])
            student_skills = execute_query(
                "SELECT skill_id FROM student_skills WHERE user_id = %s",
                (current_user.id,),
                fetch='all'
            ) or []
            s_ids = {s['skill_id'] for s in student_skills}
            r['matched_skills'] = [s for s in career_skills if s['id'] in s_ids]
            r['missing_skills'] = [s for s in career_skills if s['id'] not in s_ids]
            r['match_pct'] = int(round((len(r['matched_skills']) / max(1, len(career_skills))) * 100))

    return render_template('recommendations.html', recommendations=results)

@recommendations_bp.route('/skill-gap')
@login_required
def skill_gap():
    career_id = request.args.get('career_id', type=int)
    if not career_id:
        career_id = _get_student_base_career_id()

    analysis = explainer_service.get_skill_gap_analysis(current_user.id, career_id)
    recommended_careers = _get_recommended_career_options()

    if not analysis:
        flash('Career profile not found for gap analysis.', 'error')
        return redirect(url_for('recommendations.get_recommendations'))

    career_obj = {
        'id': career_id,
        'title': analysis['career']['title'],
        'score': analysis['summary']['match_percentage'] / 100.0
    }

    return render_template(
        'skill_gap.html',
        analysis=analysis,
        career=career_obj,
        recommended_careers=recommended_careers,
        selected_career_id=career_id
    )

@recommendations_bp.route('/alternative-careers')
@login_required
def alternative_careers():
    career_id = request.args.get('career_id', type=int)
    if not career_id:
        career_id = _get_student_base_career_id()

    top_career, alternatives = alt_engine.get_alternative_careers(career_id, top_n=4)
    recommended_careers = _get_recommended_career_options()

    return render_template(
        'alternative_careers.html',
        top_career=top_career,
        alternatives=alternatives,
        recommended_careers=recommended_careers,
        selected_career_id=career_id
    )

@recommendations_bp.route('/learning-path')
@login_required
def learning_path():
    career_id = request.args.get('career_id', type=int)
    if not career_id:
        career_id = _get_student_base_career_id()

    path_data = path_engine.generate_learning_path(current_user.id, career_id)
    recommended_careers = _get_recommended_career_options()

    if not path_data:
        flash('Career not found for learning path generation.', 'error')
        return redirect(url_for('recommendations.get_recommendations'))

    return render_template(
        'learning_path.html',
        path=path_data,
        recommended_careers=recommended_careers,
        selected_career_id=career_id
    )

@recommendations_bp.route('/graph')
@login_required
def view_graph():
    stats = kg.get_stats()
    graph_data = kg.get_graph_data(limit_nodes=100)
    return render_template('knowledge_graph.html', stats=stats, graph_data=graph_data)

@recommendations_bp.route('/history')
@login_required
def history():
    recs = execute_query(
        """SELECT DATE(created_at) as rec_date, COUNT(*) as career_count, MAX(hybrid_score) as max_score
           FROM recommendations
           WHERE user_id = %s
           GROUP BY DATE(created_at)
           ORDER BY rec_date DESC""",
        (current_user.id,),
        fetch='all'
    ) or []

    if not recs:
        # Default mock record for new user
        recs = [{
            'rec_date': 'Current Session',
            'career_count': 5,
            'max_score': 0.88
        }]

    return render_template('history.html', history=recs)

