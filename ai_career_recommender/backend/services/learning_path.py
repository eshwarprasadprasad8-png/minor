from database.connection import execute_query
from graph.knowledge_graph import KnowledgeGraph

class LearningPathEngine:
    def __init__(self):
        self.kg = KnowledgeGraph.get_instance()

    def generate_learning_path(self, user_id, career_id):
        career = execute_query(
            "SELECT id, title, category, description, average_salary FROM careers WHERE id = %s",
            (career_id,),
            fetch='one'
        )
        if not career:
            return None

        # Fetch student's current skills
        student_skills = execute_query(
            "SELECT skill_id FROM student_skills WHERE user_id = %s",
            (user_id,),
            fetch='all'
        ) or []
        acquired_ids = set(s['skill_id'] for s in student_skills)

        # Career required skills
        career_skills = self.kg.get_career_skills(career_id)
        missing_skills = [s for s in career_skills if s['id'] not in acquired_ids]

        if not missing_skills:
            # If all acquired, show advanced mastery track
            missing_skills = career_skills

        missing_skill_ids = [s['id'] for s in missing_skills]
        ordered_ids = self.kg.get_prerequisite_order(missing_skill_ids)

        skill_map = {s['id']: s for s in missing_skills}
        ordered_skills = [skill_map[sid] for sid in ordered_ids if sid in skill_map]

        # Partition into phases
        phases = [
            {'title': 'Phase 1: Foundations & Core Prerequisites', 'skills': [], 'duration_weeks': 4, 'icon': 'fa-solid fa-seedling text-success'},
            {'title': 'Phase 2: Domain Architecture & Specialized Tools', 'skills': [], 'duration_weeks': 6, 'icon': 'fa-solid fa-code text-cyan'},
            {'title': 'Phase 3: Production Mastery & Capstone Implementation', 'skills': [], 'duration_weeks': 8, 'icon': 'fa-solid fa-rocket text-purple'}
        ]

        total_items = len(ordered_skills)
        for idx, skill in enumerate(ordered_skills):
            diff = skill.get('difficulty', 'Intermediate')
            if diff == 'Beginner' or idx < total_items // 3:
                target_phase = 0
            elif diff == 'Intermediate' or idx < (2 * total_items) // 3:
                target_phase = 1
            else:
                target_phase = 2

            skill_entry = {
                'id': skill['id'],
                'name': skill['name'],
                'category': skill.get('category', 'General'),
                'difficulty': diff,
                'importance': skill.get('importance', 0.8),
                'estimated_hours': 25 if diff == 'Beginner' else (45 if diff == 'Intermediate' else 70),
                'resources': [
                    {'name': f'Official {skill["name"]} Documentation', 'type': 'Documentation'},
                    {'name': f'Interactive Hands-on Labs & Coding Exercises', 'type': 'Practical'}
                ],
                'project_idea': f"Build an end-to-end portfolio module demonstrating {skill['name']} in {career['title']} workflows."
            }
            phases[target_phase]['skills'].append(skill_entry)

        # Remove empty phases if any
        active_phases = [p for p in phases if p['skills']]
        total_weeks = sum(p['duration_weeks'] for p in active_phases)

        return {
            'career': career,
            'total_skills_to_learn': len(ordered_skills),
            'total_duration_weeks': total_weeks,
            'phases': active_phases
        }

