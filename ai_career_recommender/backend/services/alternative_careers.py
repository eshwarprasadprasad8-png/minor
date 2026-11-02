import numpy as np
from database.connection import execute_query
from graph.knowledge_graph import KnowledgeGraph
from gnn.predict import GNNPredictor

class AlternativeCareersEngine:
    def __init__(self):
        self.kg = KnowledgeGraph.get_instance()
        self.gnn = GNNPredictor.get_instance()

    def get_alternative_careers(self, base_career_id, top_n=4):
        base_career = execute_query(
            "SELECT id, title, category, description, average_salary, job_outlook FROM careers WHERE id = %s",
            (base_career_id,),
            fetch='one'
        )
        if not base_career:
            return None, []

        all_careers = execute_query(
            "SELECT id, title, category, description, average_salary, job_outlook FROM careers WHERE id != %s",
            (base_career_id,),
            fetch='all'
        ) or []

        base_skills = {s['id']: s for s in self.kg.get_career_skills(base_career_id)}
        base_skill_ids = set(base_skills.keys())
        base_gnn_vec = self.gnn.get_career_embedding(base_career_id)
        norm_base_gnn = np.linalg.norm(base_gnn_vec)

        scored_alternatives = []

        for c in all_careers:
            c_id = c['id']
            cand_skills = {s['id']: s for s in self.kg.get_career_skills(c_id)}
            cand_skill_ids = set(cand_skills.keys())

            # 1. Graph Jaccard Similarity
            s_graph = self.kg.get_jaccard_similarity(base_career_id, c_id)

            # 2. GNN Embedding Cosine Similarity
            cand_gnn_vec = self.gnn.get_career_embedding(c_id)
            norm_cand_gnn = np.linalg.norm(cand_gnn_vec)
            if norm_base_gnn > 1e-6 and norm_cand_gnn > 1e-6:
                cos_sim = float(np.dot(base_gnn_vec, cand_gnn_vec) / (norm_base_gnn * norm_cand_gnn))
                s_gnn = max(0.1, min(0.99, (cos_sim + 1.0) / 2.0))
            else:
                s_gnn = 0.5

            # 3. ML Domain/Category Similarity
            shared_ids = base_skill_ids & cand_skill_ids
            additional_ids = cand_skill_ids - base_skill_ids
            category_match = 1.0 if c.get('category') == base_career.get('category') else 0.4
            overlap_ratio = len(shared_ids) / max(1, len(cand_skill_ids))
            s_ml = 0.6 * overlap_ratio + 0.4 * category_match

            # Multi-Modal Combined Similarity
            s_sim = (0.40 * s_gnn) + (0.35 * s_graph) + (0.25 * s_ml)
            similarity_pct = int(round(s_sim * 100))

            # Transition Effort Assessment
            add_count = len(additional_ids)
            if add_count <= 2:
                effort = "Low"
                badge = "success"
            elif add_count <= 4:
                effort = "Medium"
                badge = "warning"
            else:
                effort = "High"
                badge = "danger"

            shared_skill_objs = [cand_skills[sid] for sid in shared_ids]
            additional_skill_objs = [cand_skills[sid] for sid in additional_ids]

            scored_alternatives.append({
                'career_id': c_id,
                'title': c['title'],
                'category': c.get('category', 'General'),
                'description': c.get('description', ''),
                'similarity_pct': similarity_pct,
                's_sim': s_sim,
                'gnn_similarity': round(s_gnn, 2),
                'graph_similarity': round(s_graph, 2),
                'ml_similarity': round(s_ml, 2),
                'transition_effort': effort,
                'transition_effort_badge': badge,
                'shared_skills': shared_skill_objs,
                'shared_skills_count': len(shared_skill_objs),
                'additional_skills': additional_skill_objs,
                'additional_skills_count': len(additional_skill_objs),
                'average_salary': c.get('average_salary', '$85,000'),
                'job_demand': c.get('job_outlook', 'High Demand (12% growth)')
            })

        scored_alternatives.sort(key=lambda x: x['s_sim'], reverse=True)
        return base_career, scored_alternatives[:top_n]

