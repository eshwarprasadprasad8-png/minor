from database.connection import execute_query
from graph.knowledge_graph import KnowledgeGraph

class ExplainerService:
    def __init__(self):
        self.kg = KnowledgeGraph.get_instance()

    def get_skill_gap_analysis(self, user_id, career_id):
        career = execute_query(
            "SELECT id, title, category, description, average_salary, job_outlook FROM careers WHERE id = %s",
            (career_id,),
            fetch='one'
        )
        if not career:
            return None

        # Fetch student's acquired skills
        student_skills_rows = execute_query(
            "SELECT skill_id, proficiency_level FROM student_skills WHERE user_id = %s",
            (user_id,),
            fetch='all'
        ) or []
        student_skills = {r['skill_id']: r.get('proficiency_level', 'Intermediate') for r in student_skills_rows}

        # Fetch required skills for career
        required_skills = self.kg.get_career_skills(career_id)

        prof_to_pct = {
            'None': 0,
            'Beginner': 35,
            'Intermediate': 70,
            'Advanced': 100
        }

        analyzed_skills = []
        complete_count = 0
        partial_count = 0
        missing_count = 0

        for s in required_skills:
            s_id = s['id']
            diff = s.get('difficulty', 'Intermediate')
            req_prof = 'Advanced' if diff == 'Advanced' else 'Intermediate'
            req_pct = prof_to_pct.get(req_prof, 70)

            cur_prof = student_skills.get(s_id, 'None')
            cur_pct = prof_to_pct.get(cur_prof, 0)
            gap = max(0, req_pct - cur_pct)

            # Determine status & priority
            importance = float(s.get('importance', 0.8))
            if cur_pct >= req_pct:
                status = 'Complete'
                complete_count += 1
                priority = 'Low'
            elif cur_pct > 0:
                status = 'Partial'
                partial_count += 1
                priority = 'High' if importance >= 0.8 else 'Medium'
            else:
                missing_count += 1
                if importance >= 0.85 or diff == 'Advanced':
                    status = 'Major Gap'
                    priority = 'Critical'
                else:
                    status = 'Gap'
                    priority = 'High'

            analyzed_skills.append({
                'id': s_id,
                'name': s['name'],
                'category': s.get('category', 'General'),
                'difficulty': diff,
                'importance': importance,
                'priority_label': priority,
                'current_proficiency': cur_prof,
                'required_proficiency': req_prof,
                'current_pct': cur_pct,
                'required_pct': req_pct,
                'gap': gap,
                'status': status
            })

        # Sort: Critical -> High -> Medium -> Low
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        analyzed_skills.sort(key=lambda x: (priority_order.get(x['priority_label'], 4), -x['importance']))

        total_req = len(required_skills)
        match_percentage = int(round((complete_count / max(1, total_req)) * 100)) if total_req > 0 else 0
        high_priority = [s for s in analyzed_skills if s['priority_label'] in ['Critical', 'High']]

        return {
            'career': career,
            'summary': {
                'match_percentage': match_percentage,
                'total_required': total_req,
                'complete_count': complete_count,
                'partial_count': partial_count,
                'missing_count': missing_count,
                'high_priority_skills': high_priority
            },
            'skills': analyzed_skills
        }

