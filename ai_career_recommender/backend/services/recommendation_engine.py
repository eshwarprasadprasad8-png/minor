from config import Config
from database.connection import execute_query
from ml.recommender import ContentRecommender
from gnn.predict import GNNPredictor
from graph.knowledge_graph import KnowledgeGraph

class RecommendationEngine:
    def __init__(self):
        self.ml_recommender = ContentRecommender()
        self.gnn_predictor = GNNPredictor.get_instance()
        self.kg = KnowledgeGraph.get_instance()

    def generate_recommendations(self, user_id, top_k=None, persist=True):
        if top_k is None:
            top_k = Config.TOP_K_RECOMMENDATIONS

        # 1. Fetch Student Profile details
        profile = execute_query(
            "SELECT * FROM student_profiles WHERE user_id = %s",
            (user_id,),
            fetch='one'
        ) or {}

        # 2. Fetch Student Verified Skills
        student_skills = execute_query(
            "SELECT skill_id, proficiency_level FROM student_skills WHERE user_id = %s",
            (user_id,),
            fetch='all'
        ) or []
        student_skill_ids = [s['skill_id'] for s in student_skills]

        # 3. Fetch Student Interests
        student_interests = execute_query(
            "SELECT interest_id FROM student_interests WHERE user_id = %s",
            (user_id,),
            fetch='all'
        ) or []
        student_interest_ids = [i['interest_id'] for i in student_interests]

        degree = profile.get('degree', '')
        branch = profile.get('branch', '')

        # 4. Compute ML & GNN scores
        ml_scores = self.ml_recommender.compute_ml_scores(student_skill_ids, student_interest_ids, degree, branch)
        gnn_scores = self.gnn_predictor.compute_gnn_scores(student_skill_ids, student_interest_ids)

        # 5. Fetch all careers metadata
        careers = execute_query("SELECT id, title, category, description, average_salary, job_outlook FROM careers", fetch='all') or []
        careers_by_id = {c['id']: c for c in careers}

        # 6. Hybrid Score Computation
        ml_weight = Config.ML_WEIGHT
        gnn_weight = Config.GNN_WEIGHT
        scored_candidates = []

        for c_id, c in careers_by_id.items():
            s_ml = ml_scores.get(c_id, 0.5)
            s_gnn = gnn_scores.get(c_id, 0.5)
            hybrid_score = (ml_weight * s_ml) + (gnn_weight * s_gnn)
            scored_candidates.append({
                'career_id': c_id,
                'title': c['title'],
                'category': c.get('category', 'General'),
                'description': c.get('description', ''),
                'average_salary': c.get('average_salary', '$85,000'),
                'job_outlook': c.get('job_outlook', 'High Demand'),
                'ml_score': round(s_ml, 4),
                'gnn_score': round(s_gnn, 4),
                'hybrid_score': round(hybrid_score, 4)
            })

        # Initial sort by raw hybrid score descending
        scored_candidates.sort(key=lambda x: x['hybrid_score'], reverse=True)

        # 7. MMR Diversity Filtering
        diversity_penalty = Config.DIVERSITY_PENALTY
        max_same_category = Config.MAX_SAME_CATEGORY_LIMIT
        category_counts = {}
        ranked_results = []

        remaining = list(scored_candidates)
        while remaining and len(ranked_results) < top_k:
            best_idx = 0
            best_penalized_score = -999.0

            for idx, cand in enumerate(remaining):
                cat = cand['category']
                current_count = category_counts.get(cat, 0)
                # Apply penalty if category appears >= limit
                penalty = (max(0, current_count - max_same_category + 1) * diversity_penalty) if current_count >= max_same_category else 0.0
                adj_score = cand['hybrid_score'] - penalty

                if adj_score > best_penalized_score:
                    best_penalized_score = adj_score
                    best_idx = idx

            selected = remaining.pop(best_idx)
            selected['rank_position'] = len(ranked_results) + 1
            cat = selected['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
            ranked_results.append(selected)

        # 8. Enrich results with explanation & skill gaps
        for item in ranked_results:
            c_id = item['career_id']
            career_skills = self.kg.get_career_skills(c_id)
            matched = [s for s in career_skills if s['id'] in student_skill_ids]
            missing = [s for s in career_skills if s['id'] not in student_skill_ids]

            item['matched_skills'] = matched
            item['missing_skills'] = missing
            item['match_pct'] = int(round((len(matched) / max(1, len(career_skills))) * 100))
            
            # Text justification
            exp_text = f"Strong alignment in {item['category']} with {len(matched)} of {len(career_skills)} key skills mastered. "
            if missing:
                missing_names = ", ".join(s['name'] for s in missing[:3])
                exp_text += f"Prioritize acquiring: {missing_names}."
            else:
                exp_text += "Complete foundational skill profile achieved!"
            item['explanation'] = exp_text

        # 9. Persist to recommendations and skill_gaps tables
        if persist:
            try:
                execute_query("DELETE FROM recommendations WHERE user_id = %s", (user_id,), commit=True)
                execute_query("DELETE FROM skill_gaps WHERE user_id = %s", (user_id,), commit=True)

                for item in ranked_results:
                    execute_query(
                        """INSERT INTO recommendations 
                           (user_id, career_id, hybrid_score, ml_score, gnn_score, rank_position, explanation)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (user_id, item['career_id'], item['hybrid_score'], item['ml_score'], item['gnn_score'], item['rank_position'], item['explanation']),
                        commit=True
                    )

                    # Save skill gaps for this recommendation
                    for s in item['matched_skills']:
                        execute_query(
                            "INSERT INTO skill_gaps (user_id, career_id, skill_id, status, importance) VALUES (%s, %s, %s, %s, %s)",
                            (user_id, item['career_id'], s['id'], 'acquired', s.get('importance', 0.8)),
                            commit=True
                        )
                    for s in item['missing_skills']:
                        execute_query(
                            "INSERT INTO skill_gaps (user_id, career_id, skill_id, status, importance) VALUES (%s, %s, %s, %s, %s)",
                            (user_id, item['career_id'], s['id'], 'missing', s.get('importance', 0.8)),
                            commit=True
                        )
            except Exception as e:
                print(f"[!] Warning persisting recommendations: {e}")

        return ranked_results

