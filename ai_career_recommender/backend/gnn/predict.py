import os
import torch
import numpy as np
from graph.knowledge_graph import KnowledgeGraph
from gnn.model import GraphSAGEModel

class GNNPredictor:
    _instance = None

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.node_to_idx = {}
        self.idx_to_node = {}
        self.embeddings = None
        self.model = None
        self._initialize_gnn()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _initialize_gnn(self):
        kg = KnowledgeGraph.get_instance()
        nodes = list(kg.graph.nodes(data=True))
        num_nodes = len(nodes)
        
        if num_nodes == 0:
            return

        self.node_to_idx = {n: i for i, (n, _) in enumerate(nodes)}
        self.idx_to_node = {i: n for i, (n, _) in enumerate(nodes)}

        # Build initial feature matrix X of shape (num_nodes, 64)
        x_features = []
        for n, data in nodes:
            n_type = data.get('node_type', '')
            vec = [0.0] * 64
            # One-hot node type (0..3)
            if n_type == 'career':
                vec[0] = 1.0
            elif n_type == 'skill':
                vec[1] = 1.0
            elif n_type == 'interest':
                vec[2] = 1.0
            elif n_type == 'education':
                vec[3] = 1.0
            
            # Centrality / Degree features (4..7)
            deg = float(kg.graph.degree(n))
            vec[4] = min(deg / 20.0, 1.0)
            in_deg = float(kg.graph.in_degree(n)) if kg.graph.is_directed() else deg
            vec[5] = min(in_deg / 20.0, 1.0)
            
            # Category hash projection (8..23)
            cat_hash = hash(data.get('category', 'General')) % 16
            vec[8 + cat_hash] = 1.0

            # Difficulty encoding for skills (24..26)
            diff = data.get('difficulty', '')
            if diff == 'Beginner':
                vec[24] = 1.0
            elif diff == 'Intermediate':
                vec[25] = 1.0
            elif diff == 'Advanced':
                vec[26] = 1.0

            x_features.append(vec)

        x_tensor = torch.tensor(x_features, dtype=torch.float32, device=self.device)

        # Build edge_index tensor
        src_indices = []
        dst_indices = []
        for u, v in kg.graph.edges():
            if u in self.node_to_idx and v in self.node_to_idx:
                src_indices.append(self.node_to_idx[u])
                dst_indices.append(self.node_to_idx[v])
                # Add reciprocal edge for undirected message passing
                src_indices.append(self.node_to_idx[v])
                dst_indices.append(self.node_to_idx[u])

        if not src_indices:
            src_indices = [0]
            dst_indices = [0]

        edge_index = torch.tensor([src_indices, dst_indices], dtype=torch.long, device=self.device)

        # Initialize model with deterministic seed
        torch.manual_seed(42)
        self.model = GraphSAGEModel(in_channels=64, hidden_channels=48, out_channels=32).to(self.device)
        self.model.eval()

        with torch.no_grad():
            self.embeddings = self.model(x_tensor, edge_index).cpu().numpy()

    def get_node_embedding(self, node_key):
        if self.embeddings is None or node_key not in self.node_to_idx:
            return np.zeros(32, dtype=np.float32)
        idx = self.node_to_idx[node_key]
        return self.embeddings[idx]

    def get_career_embedding(self, career_id):
        return self.get_node_embedding(f"career_{career_id}")

    def compute_gnn_scores(self, student_skill_ids, student_interest_ids=None):
        """
        Computes inductive GNN similarity between student profile embedding and career nodes.
        Returns dict {career_id: gnn_score, ...}
        """
        if self.embeddings is None:
            self._initialize_gnn()

        student_skill_ids = student_skill_ids or []
        student_interest_ids = student_interest_ids or []

        # 1. Gather component embeddings
        skill_vectors = [self.get_node_embedding(f"skill_{s_id}") for s_id in student_skill_ids]
        interest_vectors = [self.get_node_embedding(f"interest_{i_id}") for i_id in student_interest_ids]

        # 2. Inductive student representation
        if skill_vectors:
            s_mean = np.mean(skill_vectors, axis=0)
        else:
            s_mean = np.zeros(32, dtype=np.float32)

        if interest_vectors:
            i_mean = np.mean(interest_vectors, axis=0)
        else:
            i_mean = np.zeros(32, dtype=np.float32)

        z_student = s_mean + (0.5 * i_mean)
        norm_s = np.linalg.norm(z_student)

        # Fallback if student profile is empty
        if norm_s > 1e-6:
            z_student = z_student / norm_s

        kg = KnowledgeGraph.get_instance()
        career_nodes = [(n, d['raw_id']) for n, d in kg.graph.nodes(data=True) if d.get('node_type') == 'career']

        scores = {}
        for node_key, c_id in career_nodes:
            z_career = self.get_node_embedding(node_key)
            norm_c = np.linalg.norm(z_career)
            if norm_s > 1e-6 and norm_c > 1e-6:
                # Cosine similarity
                sim = float(np.dot(z_student, z_career) / (norm_s * norm_c))
                # Map from [-1, 1] to [0.1, 0.98]
                score = 0.5 + (0.48 * sim)
            else:
                score = 0.50
            scores[c_id] = round(float(np.clip(score, 0.05, 0.99)), 4)

        return scores

