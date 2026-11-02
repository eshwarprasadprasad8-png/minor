import networkx as nx
from database.connection import execute_query

class KnowledgeGraph:
    _instance = None

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_graph()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _build_graph(self):
        self.graph.clear()

        # 1. Add Career Nodes
        careers = execute_query("SELECT id, title, category FROM careers", fetch='all') or []
        for c in careers:
            self.graph.add_node(
                f"career_{c['id']}",
                node_type='career',
                raw_id=c['id'],
                label=c['title'],
                category=c.get('category', 'General')
            )

        # 2. Add Skill Nodes
        skills = execute_query("SELECT id, name, category, difficulty_level FROM skills", fetch='all') or []
        for s in skills:
            self.graph.add_node(
                f"skill_{s['id']}",
                node_type='skill',
                raw_id=s['id'],
                label=s['name'],
                category=s.get('category', 'General'),
                difficulty=s.get('difficulty_level', 'Beginner')
            )

        # 3. Add Interest Nodes
        interests = execute_query("SELECT id, name FROM interests", fetch='all') or []
        for i in interests:
            self.graph.add_node(
                f"interest_{i['id']}",
                node_type='interest',
                raw_id=i['id'],
                label=i['name']
            )

        # 4. Add Career-Skill Edges
        career_skills = execute_query(
            "SELECT career_id, skill_id, importance, skill_type FROM career_skills",
            fetch='all'
        ) or []
        for cs in career_skills:
            c_node = f"career_{cs['career_id']}"
            s_node = f"skill_{cs['skill_id']}"
            if self.graph.has_node(c_node) and self.graph.has_node(s_node):
                self.graph.add_edge(
                    c_node,
                    s_node,
                    rel_type='requires',
                    weight=float(cs.get('importance', 0.8)),
                    skill_type=cs.get('skill_type', 'Required')
                )

        # 5. Add Skill-Skill Prerequisite Edges (Ontology Rules)
        # Define logical prerequisite relationships between foundational and advanced skills
        prereqs = [
            # Python foundation
            ("Python", "Machine Learning Algorithms"),
            ("Python", "Pandas"),
            ("Python", "NumPy"),
            ("Python", "Flask"),
            ("Python", "FastAPI"),
            ("Python", "Django"),
            ("Machine Learning Algorithms", "Deep Learning"),
            ("Deep Learning", "PyTorch"),
            ("Deep Learning", "TensorFlow"),
            ("Deep Learning", "Computer Vision"),
            ("Deep Learning", "Natural Language Processing"),
            ("Deep Learning", "Graph Neural Networks"),
            ("Deep Learning", "Large Language Models (LLMs)"),
            ("Natural Language Processing", "HuggingFace & Transformers"),
            ("Computer Vision", "OpenCV"),
            ("Pandas", "Feature Engineering"),
            ("NumPy", "Statistical Modeling"),
            # Web Development
            ("HTML5 & CSS3", "JavaScript"),
            ("JavaScript", "TypeScript"),
            ("JavaScript", "React.js"),
            ("JavaScript", "Node.js"),
            ("JavaScript", "Vue.js"),
            ("React.js", "Next.js"),
            ("Node.js", "Express.js"),
            ("HTML5 & CSS3", "Tailwind CSS"),
            # DevOps & Cloud
            ("Linux Administration & Bash", "Docker & Containerization"),
            ("Docker & Containerization", "Kubernetes"),
            ("Docker & Containerization", "CI/CD Pipelines (GitHub Actions/Jenkins)"),
            ("AWS (Amazon Web Services)", "Terraform (IaC)"),
            ("Docker & Containerization", "Prometheus & Grafana"),
            # Databases
            ("SQL & Relational DBs", "PostgreSQL"),
            ("SQL & Relational DBs", "Data Pipelines (ETL)"),
            ("Data Structures & Algorithms", "Microservices Architecture"),
            ("Object-Oriented Programming (OOP)", "Software Design Patterns")
        ]

        # Name to skill node map
        name_to_node = {data['label']: node for node, data in self.graph.nodes(data=True) if data.get('node_type') == 'skill'}
        for src_name, dst_name in prereqs:
            src_node = name_to_node.get(src_name)
            dst_node = name_to_node.get(dst_name)
            if src_node and dst_node:
                self.graph.add_edge(src_node, dst_node, rel_type='prerequisite_of', weight=1.0)

    def get_career_skills(self, career_id):
        c_node = f"career_{career_id}"
        if not self.graph.has_node(c_node):
            return []
        skills = []
        for neighbor in self.graph.neighbors(c_node):
            if self.graph.nodes[neighbor].get('node_type') == 'skill':
                edge_data = self.graph.get_edge_data(c_node, neighbor) or {}
                skills.append({
                    'id': self.graph.nodes[neighbor]['raw_id'],
                    'name': self.graph.nodes[neighbor]['label'],
                    'category': self.graph.nodes[neighbor].get('category', 'General'),
                    'difficulty': self.graph.nodes[neighbor].get('difficulty', 'Beginner'),
                    'importance': edge_data.get('weight', 0.8),
                    'skill_type': edge_data.get('skill_type', 'Required')
                })
        return skills

    def get_jaccard_similarity(self, career1_id, career2_id):
        skills1 = {s['id'] for s in self.get_career_skills(career1_id)}
        skills2 = {s['id'] for s in self.get_career_skills(career2_id)}
        if not skills1 or not skills2:
            return 0.0
        intersection = len(skills1 & skills2)
        union = len(skills1 | skills2)
        return float(intersection) / float(union) if union > 0 else 0.0

    def get_prerequisite_order(self, skill_ids):
        """Topological sort of skill IDs based on prerequisite dependencies."""
        subgraph = nx.DiGraph()
        id_to_node = {s_id: f"skill_{s_id}" for s_id in skill_ids}
        nodes_set = set(id_to_node.values())

        for s_id, node in id_to_node.items():
            if self.graph.has_node(node):
                subgraph.add_node(s_id, **self.graph.nodes[node])

        for u_id, u_node in id_to_node.items():
            for v_id, v_node in id_to_node.items():
                if self.graph.has_edge(u_node, v_node):
                    subgraph.add_edge(u_id, v_id)

        try:
            ordered_ids = list(nx.topological_sort(subgraph))
        except nx.NetworkXUnfeasible:
            ordered_ids = list(skill_ids)

        return ordered_ids

    def get_stats(self):
        c_count = sum(1 for _, d in self.graph.nodes(data=True) if d.get('node_type') == 'career')
        s_count = sum(1 for _, d in self.graph.nodes(data=True) if d.get('node_type') == 'skill')
        i_count = sum(1 for _, d in self.graph.nodes(data=True) if d.get('node_type') == 'interest')
        
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'careers_count': c_count,
            'skills_count': s_count,
            'interests_count': i_count,
            'density': round(nx.density(self.graph), 4),
            'avg_degree': round(sum(d for _, d in self.graph.degree()) / max(1, self.graph.number_of_nodes()), 2)
        }

    def get_graph_data(self, limit_nodes=120):
        """Returns node and edge dictionaries for interactive JavaScript rendering."""
        nodes = []
        edges = []
        
        for n, d in list(self.graph.nodes(data=True))[:limit_nodes]:
            n_type = d.get('node_type', 'default')
            color = '#00f2fe' if n_type == 'career' else ('#4facfe' if n_type == 'skill' else '#8b5cf6')
            size = 20 if n_type == 'career' else 14
            nodes.append({
                'id': n,
                'label': d.get('label', n),
                'group': n_type,
                'color': color,
                'size': size
            })

        node_ids = {n['id'] for n in nodes}
        for u, v, d in self.graph.edges(data=True):
            if u in node_ids and v in node_ids:
                edges.append({
                    'from': u,
                    'to': v,
                    'label': d.get('rel_type', ''),
                    'arrows': 'to' if d.get('rel_type') == 'prerequisite_of' else ''
                })

        return {'nodes': nodes, 'edges': edges}

