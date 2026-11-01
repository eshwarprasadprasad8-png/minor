# AI-Based Skill & Career Recommendation System

**A Hybrid Machine Learning, Knowledge Graph, and Graph Neural Network (GNN) Engine for Student Career Navigation and Personalized Learning Paths**

---

## 1. Project Title
**AI-Based Skill & Career Recommendation System with Graph Neural Networks and Dynamic Learning Path Generation**  
*Bachelor of Engineering (B.E.) Minor Project*

---

## 2. Abstract
Navigating career pathways in modern engineering and computer science fields is challenging due to rapidly changing industry requirements, fragmented skill taxonomies, and non-linear prerequisite dependencies. Traditional recommendation engines often rely solely on flat keyword matching or collaborative filtering, ignoring the rich relational topology among skills, academic degrees, and professional domains. 

This project presents a **hybrid AI-driven recommendation platform** combining:
1. A **Content-Based Vector Recommender** using TF-IDF/Count vectorization and cosine similarity over skill requirement vectors.
2. A **Heterogeneous Knowledge Graph (KG)** modeling 167 ontology nodes (40 Careers, 102 Skills, 15 Interests, 10 Education profiles) and 948 relational edges.
3. A **PyTorch Geometric Graph Neural Network (GraphSAGE)** learning 32-dimensional inductive node embeddings and link predictions.
4. An **Explainability & Gap Analysis Engine** providing personalized reasoning and topological prerequisite ordering for custom learning paths.

---

## 3. Objectives
- **Relational Representation**: Model the multi-faceted relationships between skills, career pathways, student interests, and educational backgrounds in a unified graph ontology.
- **Hybrid Scoring**: Combine explicit requirement fulfillment (ML content scoring) with implicit structural affinity (GNN embedding cosine similarity).
- **Recommendation Diversity**: Implement category-aware penalties (Maximal Marginal Relevance) to deliver diverse Top-5 recommendations rather than identical career variations.
- **Explainable Guidance**: Generate data-grounded justifications citing the student's verified skills, academic background, and specific missing prerequisites.
- **Dynamic Learning Paths**: Topologically sort skill gaps to construct ordered, prerequisite-respecting study roadmaps with estimated durations.
- **Administrative Governance**: Provide a secure administrative dashboard for dataset maintenance, ontology relationship mapping, and audit logging.

---

## 4. Features
- **Student Profile Management**: Interactive onboarding capturing verified skills, technical interests, degree, branch, and experience levels.
- **Top-5 Hybrid Career Recommendations**: Multi-modal score combining ML ($40\%$) and GNN ($60\%$) metrics with category diversity enforcement.
- **Data-Grounded Explainability**: Transparent breakdown of recommendation factors including matched skills, aligned interests, and prioritized skill gaps.
- **Alternative Career Pathways**: Multi-modal similarity computation ($S_{sim} = 0.40 \cdot S_{gnn} + 0.35 \cdot S_{graph} + 0.25 \cdot S_{ml}$) identifying adjacent roles with shared vs. additional skill partitions.
- **Personalized Learning Path**: Dynamic topological sort over the Knowledge Graph syllabus factoring in prerequisite satisfaction, skill importance, and difficulty levels.
- **Admin Management Suite**: Full CRUD operations for careers, skills, and prerequisite relationships, plus student cohort analytics and recommendation audit trails.
- **Full Test Suite**: 40 unit and integration tests covering the entire end-to-end pipeline and edge cases.

---

## 5. Technology Stack
- **Programming Language**: Python 3.10+
- **Deep Learning & Graph Machine Learning**: PyTorch 2.0+, PyTorch Geometric (PyG) 2.3+
- **Graph & ML Algorithms**: NetworkX 3.0+, Scikit-learn 1.3+, NumPy, Pandas
- **Web Framework & Authentication**: Flask 3.0+, Flask-Login, Werkzeug Security (PBKDF2/SHA256)
- **Database & Connector**: MySQL 5.7+ / 8.0+, PyMySQL
- **Frontend Architecture**: HTML5, Vanilla CSS, Bootstrap 5.3, FontAwesome Icons

---

## 6. System Architecture

```
                               +-----------------------------+
                               |   Student User Interface    |
                               | (Profile, Skills, Interests)|
                               +--------------+--------------+
                                              |
                                              v
                               +-----------------------------+
                               |      Feature Processor      |
                               | (Sanitization & Vector Rep) |
                               +------+---------------+------+
                                      |               |
               +----------------------+               +----------------------+
               |                                                             |
               v                                                             v
+-------------------------------+                             +-------------------------------+
|     ML Content Recommender    |                             |      PyG GraphSAGE (GNN)      |
| - Requirement Weight Vector   |                             | - 32-dim Node Embeddings      |
| - Cosine Similarity Scoring   |                             | - Heterogeneous Link Predict  |
+---------------+---------------+                             +---------------+---------------+
                |                                                             |
                +----------------------+               +----------------------+
                                       |               |
                                       v               v
                               +-------------------------------+
                               |   Hybrid Ranking Engine       |
                               | Score = 0.40(ML) + 0.60(GNN)  |
                               | - Category Diversity Penalty  |
                               +---------------+---------------+
                                               |
                                               v
                               +-------------------------------+
                               |  Explainability & Gap Service |
                               |  - Matched vs Missing Skills  |
                               |  - Data-Grounded Justification|
                               +---------------+---------------+
                                               |
                                               v
                               +-------------------------------+
                               | Dynamic Learning Path Engine  |
                               | (Topological Sort Prereqs)    |
                               +-------------------------------+
```

---

## 7. Module Description

| Module Path | Core Responsibilities |
| :--- | :--- |
| [`app.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/app.py) | Application factory, blueprint registration, session loader, root routing. |
| [`config.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/config.py) | Environment configuration loader with fallback defaults. |
| [`database/connection.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/database/connection.py) | Thread-safe connection pool, query execution, and rollback management. |
| [`graph/knowledge_graph.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/graph/knowledge_graph.py) | NetworkX heterogeneous graph builder, neighborhood search, graph metrics. |
| [`gnn/graph_data.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/gnn/graph_data.py) | PyG `Data` transformation, node type mapping, train/val edge splitting. |
| [`gnn/model.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/gnn/model.py) | 2-layer GraphSAGE architecture with link prediction dot-product decoder. |
| [`gnn/train.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/gnn/train.py) | Inductive GNN training loop, BCE with logits loss, embedding persistence. |
| [`gnn/predict.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/gnn/predict.py) | Composite student profile embedding calculation and career scoring. |
| [`ml/recommender.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/ml/recommender.py) | Content-based skill requirement vector matching and education alignment. |
| [`services/recommendation_engine.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/services/recommendation_engine.py) | Hybrid linear scoring, MMR diversity filtering, Top-5 ranker. |
| [`services/alternative_careers.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/services/alternative_careers.py) | Cross-career similarity ($S_{gnn}, S_{graph}, S_{ml}$) & skill partitioning. |
| [`services/learning_path.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/services/learning_path.py) | Directed prerequisite graph traversal, topological sort, timeline estimator. |
| [`services/explainer.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/services/explainer.py) | Dynamic evidence derivation and personalized checklist generation. |
| [`routes/admin.py`](file:///c:/Users/Eshwar/Desktop/minor/ai_career_recommender/routes/admin.py) | RBAC-guarded routes for Careers, Skills, Mappings, Cohorts, and Audits. |

---

## 8. Dataset Description

The dataset resides in `data/` and comprises 7 normalized CSV tables:
1. `careers.csv`: 40 standardized career roles spanning 7 domains (AI/ML, Web, Cloud/DevOps, Cyber Security, Data Science, Mobile, Systems).
2. `skills.csv`: 102 technical and professional skills with difficulty classifications (`Beginner`, `Intermediate`, `Advanced`).
3. `career_skills.csv`: 468 requirement mappings with continuous importance weights ($0.1 \le w \le 1.0$) and requirement types (`Required`, `Preferred`).
4. `interests.csv`: 15 domain interest tracks.
5. `education.csv`: 10 academic degree/branch requirements.
6. `job_market.csv`: 40 market growth and demand indicators.
7. `student_profiles.csv`: 50 synthesized benchmark student profiles.

> **Synthetic Dataset Disclaimer**:  
> All dataset tables are synthetically designed for academic demonstration and simulation purposes in a B.E. minor project. Real-world commercial applications should retrain on live job market records (e.g. O*NET, LinkedIn, Lightcast).

---

## 9. Machine Learning Methodology
The Content-Based Recommender models each career $c_j$ as a target requirement vector $\mathbf{v}_{c_j} \in \mathbb{R}^{|S|}$, where each dimension represents the importance weight of skill $s_i$. 

A student's profile is transformed into a binary/proficiency vector $\mathbf{u} \in \mathbb{R}^{|S|}$. The baseline skill match score is computed as:

$$\text{SkillScore}(u, c_j) = \frac{\sum_{s \in u \cap c_j} w_{c_j, s}}{\sum_{s \in c_j} w_{c_j, s}}$$

Additional bonus factors are awarded for interest matches ($+0.05$ per aligned interest) and education qualification ($+0.10$ for compatible degree/branch). The resulting score is clipped to $[0.0, 1.0]$.

---

## 10. Knowledge Graph Methodology
The Knowledge Graph $G = (V, E)$ is constructed using NetworkX:
- **Node Types**: $V = V_{\text{career}} \cup V_{\text{skill}} \cup V_{\text{interest}} \cup V_{\text{education}}$ ($|V| = 167$)
- **Edge Types**: 
  - $(\text{Career}, \text{Skill})$: Requirement relation with weight $w$
  - $(\text{Career}, \text{Interest})$: Domain alignment
  - $(\text{Career}, \text{Education})$: Eligibility criterion
  - $(\text{Skill}, \text{Skill})$: Prerequisite dependency ($s_a \to s_b$)

The Knowledge Graph enables structural neighborhood queries, Jaccard similarity between roles ($J(c_1, c_2) = \frac{|S(c_1) \cap S(c_2)|}{|S(c_1) \cup S(c_2)|}$), and topological sorting for learning pathways.

---

## 11. Graph Neural Network (GNN) Methodology
We implement a **GraphSAGE (Graph Sample and Aggregate)** architecture in PyTorch Geometric:

1. **Graph Representation**:
   - Initial 64-dimensional feature representations: One-hot encoded node types combined with normalized node degree and centrality metrics.
2. **Neighborhood Aggregation**:
   For layer $k \in \{1, 2\}$, node embedding $\mathbf{h}_v^{(k)}$ is updated via mean neighborhood aggregation:
   $$\mathbf{h}_{\mathcal{N}(v)}^{(k)} = \text{MEAN}\left(\{\mathbf{h}_u^{(k-1)}, \forall u \in \mathcal{N}(v)\}\right)$$
   $$\mathbf{h}_v^{(k)} = \sigma\left(\mathbf{W}^{(k)} \cdot \left[\mathbf{h}_v^{(k-1)} \,\|\, \mathbf{h}_{\mathcal{N}(v)}^{(k)}\right]\right)$$
3. **Training Objective**:
   Trained via positive and negative edge sampling using Binary Cross-Entropy with Logits:
   $$\mathcal{L} = -\sum_{(u, v) \in \mathcal{E}_{\text{pos}}} \log \sigma(\mathbf{z}_u^\top \mathbf{z}_v) - \sum_{(u, v') \in \mathcal{E}_{\text{neg}}} \log (1 - \sigma(\mathbf{z}_u^\top \mathbf{z}_{v'}))$$
4. **Inductive Student Scoring**:
   A student profile's latent representation $\mathbf{z}_{\text{student}}$ is computed by aggregating embeddings of their verified skills, interests, and education:
   $$\mathbf{z}_{\text{student}} = \frac{1}{|S_u|} \sum_{s \in S_u} \mathbf{z}_s + 0.5 \sum_{i \in I_u} \mathbf{z}_i + 0.3 \mathbf{z}_{\text{edu}}$$
   Career affinity is computed via Cosine Similarity:
   $$\text{Score}_{\text{GNN}}(u, c) = \frac{\mathbf{z}_{\text{student}} \cdot \mathbf{z}_c}{\|\mathbf{z}_{\text{student}}\| \|\mathbf{z}_c\|}$$

---

## 12. Recommendation & Diversity Methodology
The final hybrid score combines the ML content score and GNN structural affinity:

$$\text{Score}_{\text{hybrid}}(u, c) = (0.40 \cdot \text{Score}_{\text{ML}}) + (0.60 \cdot \text{Score}_{\text{GNN}})$$

### Diversity Filtering (Maximal Marginal Relevance)
To prevent recommendations from being saturated by 5 almost-identical roles in the same domain (e.g. 5 frontend web titles), a **category penalty** ($\lambda = 0.15$) is applied if a career belongs to a category that has already appeared $\ge 2$ times in the Top-K selection:

$$\text{Score}_{\text{final}}(c) = \text{Score}_{\text{hybrid}}(c) - (\text{count}(\text{category}_c) \times \lambda)$$

---

## 13. Database Design
The relational MySQL schema maintains normalized entities and audit logs:
- `users`: ID, username, email, password hash, role (`student`/`admin`).
- `student_profiles`: Bio, degree, branch, graduation year, experience level, target career.
- `skills`: Skill ID, name, category, difficulty level.
- `careers`: Career ID, title, category, description, salary range, job demand.
- `career_skills`: Join table with `importance` ($0.1-1.0$) and `skill_type`.
- `student_skills`: Acquired student skill relationships.
- `student_interests`: Declared student domain interests.
- `education`: Degree/branch career eligibility mapping.
- `recommendations`: Historical recommendation audit log with scores and explainability text.
- `skill_gaps`: Individual missing vs matching skill breakdown per recommendation run.

---

## 14. Project Structure & Partitioning

```
ai_career_recommender/
├── backend/                        # Application logic, AI models, database & APIs
│   ├── app.py                      # Flask Application Factory
│   ├── run.py                      # Server launcher
│   ├── config.py                   # App & database configuration
│   ├── init_db.py                  # Automated MySQL initialization & seeder
│   ├── seed_data.py                # Database population script
│   ├── schema.sql                  # MySQL database schema
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment credentials
│   ├── database/                   # MySQL connection handling
│   ├── models/                     # User model & auth handlers
│   ├── routes/                     # Blueprint routes (auth, student, admin, recommendations)
│   ├── services/                   # Recommendation engine, learning paths, gap analysis
│   ├── ml/                         # Content-based ML recommender
│   ├── graph/                      # NetworkX Knowledge Graph
│   ├── gnn/                        # PyTorch Geometric GNN models & weights
│   ├── data/                       # CSV datasets
│   └── tests/                      # Automated test suite
├── frontend/                       # Presentation layer
│   ├── templates/                  # Jinja2 HTML templates
│   └── static/                     # CSS stylesheets, JS scripts, and images
├── run_app.bat                     # One-click Windows runner
├── run_app.ps1                     # One-click PowerShell runner
└── README.md                       # Documentation
```

---

## 15. Installation & Setup

### Step 1: Navigate to the Backend
```powershell
cd "c:\Users\Eshwar\OneDrive\Desktop\minor\ai_career_recommender\backend"
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Verify or edit `backend/.env` with your MySQL credentials:
```ini
SECRET_KEY=ai-career-recommender-secret-key-12345
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=ai_career_recommender
DB_PORT=3306
```

---

## 16. Database Initialization (1-Step Automatic)
Ensure MySQL is running (e.g., via XAMPP or MySQL Service), then run:
```powershell
python init_db.py
```
*This automatically creates the `ai_career_recommender` database, tables from `schema.sql`, and seeds initial data and demo accounts.*

---

## 17. Model Training & Embedding Generation (Optional)
The pre-trained model weights are already provided in `backend/gnn/saved_models/`. To retrain:
```powershell
python gnn/train.py
python gnn/evaluate.py
```

---

## 18. Running the Application

### Option A: From backend directory
```powershell
python run.py
```

### Option B: From project root
```powershell
# Using PowerShell launcher:
.\run_app.ps1

# Or using Batch file (cmd / double click):
.\run_app.bat
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

### Default Demo Credentials:
- **Admin Account**: Username: `admin` | Password: `admin123`
- **Student Account**: Username: `demostudent` | Password: `student123`

---

## 19. Testing & Validation
Run the full test suite from the `backend/` directory:
```powershell
python -m unittest discover tests -v
```

### Edge Cases Covered:
- Student with zero skills selected.
- Student with large multi-domain skill portfolios (40+ skills).
- Invalid / non-existent skill IDs.
- Missing or null educational background.
- Requests for non-existent career IDs.
- Careers with empty skill requirement mappings.

---

## 19. Evaluation Metrics
The GNN and Recommendation Engine are evaluated across:
- **Link Prediction ROC-AUC**: Measures the GNN's ability to distinguish true career-skill relationships from random negative samples ($\ge 0.88$).
- **Average Precision (AP)**: Evaluates ranking precision of positive graph edges ($\ge 0.85$).
- **Top-K Hit Rate@5**: Assesses whether a student's ground-truth target role appears in the recommended Top-5 ($> 90\%$).
- **Category Entropy / Intra-List Diversity**: Verifies that the Top-5 results contain representations across multiple sub-domains.

---

## 20. Limitations
- **Synthetic Data**: The knowledge graph and user profiles are synthetically created for academic simulation and do not represent real-time live labor market dynamics.
- **Static Weighting**: The 40/60 weighting between ML and GNN is statically configured rather than learned end-to-end via reinforcement learning.
- **Synchronous Graph Updates**: Administrative additions of new skills or careers require triggering a GNN retrain to update latent node embeddings.

---

## 21. Future Enhancements
- **Dynamic GNN Fine-Tuning**: Implement online inductive inference or low-rank adaptation (LoRA) for real-time node additions without full retraining.
- **LLM-Powered Course Syllabi**: Integrate Large Language Models (LLMs) via RAG to dynamically generate week-by-week study materials and quiz assessments for missing skills.
- **Resume Parsing Engine**: Add PDF/Docx resume parser using spaCy and OCR to automatically extract acquired skills from student resumes.
- **Industry API Feeds**: Connect live APIs (e.g. LinkedIn, Indeed, GitHub) to update skill demand weights automatically based on current job postings.
