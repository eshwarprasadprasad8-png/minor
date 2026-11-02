import numpy as np
from database.connection import execute_query

class ContentRecommender:
    def __init__(self):
        pass

    def get_all_careers(self):
        return execute_query("SELECT id, title, category, description, average_salary, job_outlook FROM careers", fetch='all') or []

    def get_career_skills_map(self):
        rows = execute_query("SELECT career_id, skill_id, importance, skill_type FROM career_skills", fetch='all') or []
        career_skills = {}
        for r in rows:
            c_id = r['career_id']
            if c_id not in career_skills:
                career_skills[c_id] = {}
            career_skills[c_id][r['skill_id']] = float(r.get('importance', 0.8))
        return career_skills

    def get_education_requirements(self):
        rows = execute_query("SELECT career_id, degree, branch FROM education", fetch='all') or []
        edu_map = {}
        for r in rows:
            c_id = r['career_id']
            if c_id not in edu_map:
                edu_map[c_id] = []
            edu_map[c_id].append((r['degree'].lower(), r['branch'].lower()))
        return edu_map

    def compute_ml_scores(self, student_skill_ids, student_interest_ids=None, degree='', branch=''):
        """
        Computes weighted content match scores for all careers.
        Returns dict {career_id: ml_score, ...}
        """
        student_skill_ids = set(student_skill_ids or [])
        student_interest_ids = set(student_interest_ids or [])
        degree_clean = (degree or '').strip().lower()
        branch_clean = (branch or '').strip().lower()

        careers = self.get_all_careers()
        career_skills_map = self.get_career_skills_map()
        edu_map = self.get_education_requirements()

        # Build interest-to-category associations
        interest_rows = execute_query("SELECT id, name FROM interests", fetch='all') or []
        interest_names = {i['id']: i['name'].lower() for i in interest_rows}
        user_interest_keywords = [interest_names[i_id] for i_id in student_interest_ids if i_id in interest_names]

        scores = {}

        for c in careers:
            c_id = c['id']
            required_skills = career_skills_map.get(c_id, {})
            
            # 1. Skill requirement match
            if not required_skills:
                skill_score = 0.5
            else:
                total_weight = sum(required_skills.values())
                matched_weight = sum(w for s_id, w in required_skills.items() if s_id in student_skill_ids)
                skill_score = matched_weight / max(total_weight, 0.001)

            # 2. Education match bonus (+0.10)
            edu_bonus = 0.0
            if degree_clean or branch_clean:
                career_edus = edu_map.get(c_id, [])
                for e_deg, e_br in career_edus:
                    if degree_clean and degree_clean in e_deg:
                        edu_bonus = 0.05
                    if branch_clean and (branch_clean in e_br or e_br in branch_clean or 'any' in e_br or 'all' in e_br):
                        edu_bonus += 0.05
                        break
            edu_bonus = min(edu_bonus, 0.10)

            # 3. Interest match bonus (+0.05 per keyword alignment, up to +0.15)
            interest_bonus = 0.0
            c_cat = (c.get('category') or '').lower()
            c_title = (c.get('title') or '').lower()
            for kw in user_interest_keywords:
                # check if keyword overlaps with career title or category
                kw_tokens = kw.replace('&', ' ').replace('/', ' ').split()
                for token in kw_tokens:
                    if len(token) > 2 and (token in c_cat or token in c_title):
                        interest_bonus += 0.05
                        break
            interest_bonus = min(interest_bonus, 0.15)

            # Composite ML score
            final_ml_score = skill_score * 0.75 + edu_bonus + interest_bonus
            # Bound in [0.05, 0.99]
            final_ml_score = float(np.clip(final_ml_score, 0.05, 0.99))
            scores[c_id] = round(final_ml_score, 4)

        return scores

