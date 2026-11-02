import os
import csv

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)

# 1. Interests (15 domain tracks)
interests = [
    (1, "Artificial Intelligence & ML"),
    (2, "Full Stack Web Development"),
    (3, "Cloud Architecture & DevOps"),
    (4, "Cybersecurity & Cryptography"),
    (5, "Data Science & Big Data"),
    (6, "Mobile App Development"),
    (7, "Distributed & Systems Software"),
    (8, "Internet of Things & Robotics"),
    (9, "Blockchain & Web3"),
    (10, "Computer Vision & AR/VR"),
    (11, "Natural Language Processing"),
    (12, "Site Reliability & Networking"),
    (13, "Database Engineering"),
    (14, "Product Management & Tech Strategy"),
    (15, "UI/UX & Human Computer Interaction")
]

with open(os.path.join(data_dir, 'interests.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name'])
    for row in interests:
        writer.writerow(row)

# 2. Skills (102 skills across categories)
skills_data = [
    # AI & ML
    (1, "Python", "Programming Languages", "Intermediate"),
    (2, "PyTorch", "AI/ML", "Advanced"),
    (3, "TensorFlow", "AI/ML", "Advanced"),
    (4, "Scikit-Learn", "AI/ML", "Intermediate"),
    (5, "Machine Learning Algorithms", "AI/ML", "Intermediate"),
    (6, "Deep Learning", "AI/ML", "Advanced"),
    (7, "Natural Language Processing", "AI/ML", "Advanced"),
    (8, "Computer Vision", "AI/ML", "Advanced"),
    (9, "HuggingFace & Transformers", "AI/ML", "Intermediate"),
    (10, "MLOps & Model Deployment", "AI/ML", "Advanced"),
    (11, "Graph Neural Networks", "AI/ML", "Advanced"),
    (12, "Large Language Models (LLMs)", "AI/ML", "Advanced"),
    (13, "OpenCV", "AI/ML", "Intermediate"),
    (14, "Reinforcement Learning", "AI/ML", "Advanced"),
    
    # Data Science & Analytics
    (15, "Pandas", "Data Science", "Intermediate"),
    (16, "NumPy", "Data Science", "Intermediate"),
    (17, "SQL & Relational DBs", "Database", "Intermediate"),
    (18, "Data Visualization (Tableau/PowerBI)", "Data Science", "Beginner"),
    (19, "Statistical Modeling", "Data Science", "Advanced"),
    (20, "Apache Spark", "Big Data", "Advanced"),
    (21, "Data Pipelines (ETL)", "Data Science", "Intermediate"),
    (22, "Feature Engineering", "Data Science", "Intermediate"),
    (23, "R Programming", "Data Science", "Beginner"),
    (24, "A/B Testing & Experimentation", "Data Science", "Intermediate"),
    
    # Web & Software Development
    (25, "JavaScript", "Programming Languages", "Intermediate"),
    (26, "TypeScript", "Programming Languages", "Intermediate"),
    (27, "HTML5 & CSS3", "Web Development", "Beginner"),
    (28, "React.js", "Web Development", "Intermediate"),
    (29, "Next.js", "Web Development", "Intermediate"),
    (30, "Node.js", "Web Development", "Intermediate"),
    (31, "Express.js", "Web Development", "Intermediate"),
    (32, "FastAPI", "Web Development", "Intermediate"),
    (33, "Flask", "Web Development", "Beginner"),
    (34, "Django", "Web Development", "Intermediate"),
    (35, "RESTful API Design", "Web Development", "Intermediate"),
    (36, "GraphQL", "Web Development", "Intermediate"),
    (37, "Vue.js", "Web Development", "Beginner"),
    (38, "Tailwind CSS", "Web Development", "Beginner"),
    (39, "Microservices Architecture", "Software Engineering", "Advanced"),
    (40, "Object-Oriented Programming (OOP)", "Software Engineering", "Intermediate"),
    (41, "Data Structures & Algorithms", "Software Engineering", "Intermediate"),
    (42, "Software Design Patterns", "Software Engineering", "Advanced"),
    
    # Cloud & DevOps
    (43, "Docker & Containerization", "DevOps", "Intermediate"),
    (44, "Kubernetes", "DevOps", "Advanced"),
    (45, "AWS (Amazon Web Services)", "Cloud", "Intermediate"),
    (46, "Microsoft Azure", "Cloud", "Intermediate"),
    (47, "Google Cloud Platform (GCP)", "Cloud", "Intermediate"),
    (48, "CI/CD Pipelines (GitHub Actions/Jenkins)", "DevOps", "Intermediate"),
    (49, "Terraform (IaC)", "DevOps", "Advanced"),
    (50, "Linux Administration & Bash", "Systems", "Intermediate"),
    (51, "Prometheus & Grafana", "DevOps", "Intermediate"),
    (52, "Ansible", "DevOps", "Intermediate"),
    (53, "Git & Version Control", "Software Engineering", "Beginner"),
    (54, "Site Reliability Engineering (SRE)", "Cloud", "Advanced"),
    
    # Databases & Storage
    (55, "PostgreSQL", "Database", "Intermediate"),
    (56, "MongoDB", "Database", "Intermediate"),
    (57, "Redis & In-Memory Caching", "Database", "Intermediate"),
    (58, "Neo4j & Graph Databases", "Database", "Advanced"),
    (59, "Elasticsearch", "Database", "Intermediate"),
    (60, "Kafka & Event Streaming", "Systems", "Advanced"),
    (61, "Snowflake & Cloud Warehousing", "Data Science", "Intermediate"),
    
    # Cybersecurity
    (62, "Network Security & Protocols", "Cybersecurity", "Intermediate"),
    (63, "Penetration Testing & Ethical Hacking", "Cybersecurity", "Advanced"),
    (64, "Cryptography & PKI", "Cybersecurity", "Advanced"),
    (65, "SIEM & SOC Operations", "Cybersecurity", "Intermediate"),
    (66, "Application Security (OWASP Top 10)", "Cybersecurity", "Intermediate"),
    (67, "Wireshark & Packet Analysis", "Cybersecurity", "Intermediate"),
    (68, "Cloud Security & IAM", "Cybersecurity", "Advanced"),
    (69, "Incident Response & Forensics", "Cybersecurity", "Advanced"),
    (70, "Vulnerability Assessment", "Cybersecurity", "Intermediate"),
    
    # Mobile Development
    (71, "Flutter & Dart", "Mobile", "Intermediate"),
    (72, "React Native", "Mobile", "Intermediate"),
    (73, "Kotlin & Android SDK", "Mobile", "Intermediate"),
    (74, "Swift & iOS Development", "Mobile", "Intermediate"),
    (75, "Mobile UI Design", "Mobile", "Beginner"),
    (76, "Offline Storage (SQLite/Room)", "Mobile", "Intermediate"),
    
    # Systems & Low Level
    (77, "C++", "Programming Languages", "Advanced"),
    (78, "C Language", "Programming Languages", "Intermediate"),
    (79, "Rust", "Programming Languages", "Advanced"),
    (80, "Go (Golang)", "Programming Languages", "Intermediate"),
    (81, "Java", "Programming Languages", "Intermediate"),
    (82, "Operating Systems Internals", "Systems", "Advanced"),
    (83, "Computer Networking (TCP/IP)", "Systems", "Intermediate"),
    (84, "Concurrency & Multi-Threading", "Systems", "Advanced"),
    (85, "Embedded Systems & Microcontrollers", "Systems", "Advanced"),
    (86, "Memory Management & Profiling", "Systems", "Advanced"),
    
    # Professional & Product
    (87, "Agile & Scrum Methodologies", "Management", "Beginner"),
    (88, "Technical Writing & Docs", "General", "Beginner"),
    (89, "System Architecture Design", "Software Engineering", "Advanced"),
    (90, "Code Review & Quality Assurance", "Software Engineering", "Intermediate"),
    (91, "Unit & Integration Testing (PyTest/Jest)", "Software Engineering", "Intermediate"),
    (92, "UI/UX Prototyping (Figma)", "Design", "Beginner"),
    (93, "User Research & Usability Testing", "Design", "Beginner"),
    (94, "Product Roadmap Planning", "Management", "Intermediate"),
    (95, "Risk Assessment & Mitigation", "Management", "Intermediate"),
    (96, "DevSecOps Integration", "Cybersecurity", "Advanced"),
    (97, "Time Series Analysis", "Data Science", "Intermediate"),
    (98, "Recommendation Systems", "AI/ML", "Advanced"),
    (99, "API Gateways & Reverse Proxies", "Cloud", "Intermediate"),
    (100, "Kubernetes Helm & Operators", "DevOps", "Advanced"),
    (101, "Serverless Architecture (AWS Lambda)", "Cloud", "Intermediate"),
    (102, "Blockchain Smart Contracts (Solidity)", "Systems", "Advanced")
]

with open(os.path.join(data_dir, 'skills.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'category', 'difficulty_level'])
    for row in skills_data:
        writer.writerow(row)

# 3. Careers (40 career pathways)
careers_data = [
    (1, "Machine Learning Engineer", "AI/ML", "Designs, builds, and deploys production machine learning models, inference pipelines, and scalable predictive systems."),
    (2, "AI Research Scientist", "AI/ML", "Conducts fundamental AI/ML research in deep learning, transformer architectures, computer vision, and foundation models."),
    (3, "Data Scientist", "Data Science", "Applies statistical modeling, exploratory data analysis, and predictive algorithms to solve business problems and extract insights."),
    (4, "Data Engineer", "Data Science", "Architects robust big data pipelines, distributed warehousing, and streaming infrastructure for enterprise analytics."),
    (5, "Full Stack Web Developer", "Software Engineering", "Builds modern end-to-end web applications across front-end reactive interfaces, server APIs, and database layers."),
    (6, "Backend Software Engineer", "Software Engineering", "Engineers high-throughput server backends, microservice architectures, and robust distributed database connections."),
    (7, "Frontend Developer", "Software Engineering", "Specializes in client-facing interactive web applications, component design systems, and responsive user interfaces."),
    (8, "Cloud Solutions Architect", "Cloud & DevOps", "Architects scalable, secure, and cost-effective enterprise cloud infrastructures across multi-cloud environments."),
    (9, "DevOps & Platform Engineer", "Cloud & DevOps", "Automates CI/CD deployment pipelines, container orchestration, infrastructure as code, and runtime environments."),
    (10, "Cybersecurity Analyst", "Cyber Security", "Monitors networks, analyzes security incidents, performs vulnerability assessments, and defends critical IT assets."),
    (11, "Penetration Tester & Ethical Hacker", "Cyber Security", "Simulates cyberattacks to identify vulnerabilities in systems, networks, and web applications before malicious exploitation."),
    (12, "MLOps Engineer", "AI/ML", "Bridges the gap between machine learning model development and operational production pipelines with automated CI/CD/CT."),
    (13, "Computer Vision Engineer", "AI/ML", "Develops algorithmic pipelines for image processing, object detection, facial recognition, and video analytics."),
    (14, "NLP & Conversational AI Engineer", "AI/ML", "Constructs generative AI systems, conversational bots, semantic search, and large language model workflows."),
    (15, "Site Reliability Engineer (SRE)", "Cloud & DevOps", "Applies software engineering principles to infrastructure and operations to ensure high availability and uptime."),
    (16, "Mobile Application Developer (Flutter/React Native)", "Mobile Development", "Builds cross-platform native-performance applications for iOS and Android devices."),
    (17, "Android Native Developer", "Mobile Development", "Specializes in Kotlin-driven Android applications, mobile architecture components, and Google Play ecosystem."),
    (18, "iOS Native Developer", "Mobile Development", "Builds Apple ecosystem mobile applications using Swift, SwiftUI, Xcode, and CoreData."),
    (19, "Security Engineer", "Cyber Security", "Designs and implements enterprise security architectures, encryption standards, identity access controls, and defense layers."),
    (20, "Big Data Architect", "Data Science", "Designs enterprise data architectures using distributed computing engines like Apache Spark, Hadoop, and Kafka."),
    (21, "Systems Software Engineer", "Systems & Architecture", "Develops low-level system software, device drivers, operating system kernels, and high-performance network stacks."),
    (22, "Embedded Systems Engineer", "Systems & Architecture", "Programs firmware, microcontrollers, real-time operating systems (RTOS), and IoT hardware devices."),
    (23, "Database Administrator & Architect", "Data Science", "Manages database performance tuning, replication, clustering, high availability, and schema optimization."),
    (24, "Cloud Security Specialist", "Cyber Security", "Protects cloud computing environments, IAM policies, containerized workloads, and regulatory compliance standards."),
    (25, "Software Development Engineer in Test (SDET)", "Software Engineering", "Automates test frameworks, performance benchmarks, and quality assurance workflows across software releases."),
    (26, "API Platform Engineer", "Software Engineering", "Designs resilient REST and GraphQL APIs, developer SDKs, API gateways, and microservice communication backbones."),
    (27, "Network Architect & Engineer", "Systems & Architecture", "Plans, implements, and manages complex enterprise networking protocols, routing topologies, and data centers."),
    (28, "Blockchain Engineer", "Systems & Architecture", "Builds decentralized applications, cryptographic consensus mechanisms, and Ethereum smart contracts."),
    (29, "Game Engine Developer", "Systems & Architecture", "Programs real-time 3D graphics rendering pipelines, physics simulations, and interactive gameplay engines in C++."),
    (30, "Technical Product Manager", "Business & Product", "Guides technical product lifecycle from market discovery and architecture alignment through to user adoption."),
    (31, "UI/UX Engineer & Designer", "Software Engineering", "Translates user research and interaction workflows into accessible, intuitive, and visually stunning digital products."),
    (32, "Quantitative Developer", "Data Science", "Applies mathematical algorithms, statistical arbitrage, and ultra-low-latency financial computing techniques."),
    (33, "Business Intelligence Analyst", "Data Science", "Transforms corporate raw data into executive dashboards, business KPIs, and strategic growth recommendations."),
    (34, "Information Security Manager", "Cyber Security", "Oversees organizational cybersecurity risk governance, compliance audits (ISO/SOC2), and security teams."),
    (35, "Incident Response Specialist", "Cyber Security", "Investigates digital forensics, mitigates active cyber intrusions, and coordinates rapid disaster recovery."),
    (36, "Robotics Software Engineer", "Systems & Architecture", "Develops navigation algorithms, sensor fusion (LiDAR/SLAM), and robotic operating system (ROS) software."),
    (37, "IoT Solutions Architect", "Systems & Architecture", "Designs interconnected sensor networks, edge computing nodes, and telemetry message queuing systems."),
    (38, "DevSecOps Engineer", "Cyber Security", "Embeds automated security verification and vulnerability scanning into CI/CD continuous deployment pipelines."),
    (39, "Generative AI Application Developer", "AI/ML", "Builds autonomous agent workflows, RAG (Retrieval-Augmented Generation) pipelines, and LLM-powered applications."),
    (40, "Graph Data Scientist", "Data Science", "Specializes in knowledge graphs, network topology analytics, link prediction, and Graph Neural Networks (GNNs).")
]

with open(os.path.join(data_dir, 'careers.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'title', 'category', 'description'])
    for row in careers_data:
        writer.writerow(row)

# 4. Job market info
job_market_data = [
    (1, "125000", "Very High", "24.5"),
    (2, "140000", "High", "19.0"),
    (3, "115000", "High", "21.2"),
    (4, "120000", "Very High", "26.0"),
    (5, "105000", "Very High", "18.0"),
    (6, "112000", "High", "17.5"),
    (7, "98000", "High", "15.0"),
    (8, "135000", "Very High", "22.5"),
    (9, "122000", "Very High", "23.0"),
    (10, "102000", "Very High", "28.0"),
    (11, "118000", "High", "24.0"),
    (12, "130000", "Very High", "31.0"),
    (13, "128000", "High", "20.5"),
    (14, "132000", "Very High", "29.0"),
    (15, "125000", "Very High", "21.0"),
    (16, "104000", "High", "19.5"),
    (17, "100000", "Medium", "14.0"),
    (18, "106000", "Medium", "14.5"),
    (19, "120000", "Very High", "25.0"),
    (20, "138000", "High", "18.5"),
    (21, "116000", "Medium", "12.0"),
    (22, "96000", "Medium", "11.5"),
    (23, "95000", "Medium", "10.0"),
    (24, "126000", "Very High", "27.5"),
    (25, "95000", "Medium", "13.0"),
    (26, "114000", "High", "17.0"),
    (27, "108000", "Medium", "9.5"),
    (28, "125000", "Medium", "16.0"),
    (29, "108000", "Medium", "11.0"),
    (30, "128000", "High", "15.5"),
    (31, "92000", "High", "16.5"),
    (32, "155000", "High", "18.0"),
    (33, "88000", "Medium", "12.5"),
    (34, "135000", "High", "20.0"),
    (35, "115000", "Very High", "26.5"),
    (36, "112000", "High", "17.0"),
    (37, "120000", "High", "19.0"),
    (38, "128000", "Very High", "27.0"),
    (39, "136000", "Very High", "34.0"),
    (40, "124000", "High", "23.5")
]

with open(os.path.join(data_dir, 'job_market.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['career_id', 'avg_salary', 'demand_score', 'growth_rate_pct'])
    for row in job_market_data:
        writer.writerow(row)

# 5. Career Skills Relationships mapping (key skills for each career)
# Format: (career_id, skill_id, importance, skill_type)
career_skills_map = {
    1: [(1, 1.0, 'Required'), (2, 0.9, 'Required'), (5, 0.95, 'Required'), (6, 0.85, 'Required'), (10, 0.8, 'Preferred'), (15, 0.75, 'Required'), (16, 0.75, 'Required'), (4, 0.7, 'Required'), (53, 0.6, 'Preferred')],
    2: [(1, 1.0, 'Required'), (2, 0.95, 'Required'), (6, 0.95, 'Required'), (11, 0.85, 'Preferred'), (12, 0.85, 'Preferred'), (19, 0.9, 'Required'), (88, 0.7, 'Preferred')],
    3: [(1, 0.95, 'Required'), (15, 0.95, 'Required'), (16, 0.9, 'Required'), (17, 0.9, 'Required'), (4, 0.85, 'Required'), (19, 0.9, 'Required'), (18, 0.7, 'Preferred'), (24, 0.75, 'Preferred')],
    4: [(1, 0.9, 'Required'), (17, 0.95, 'Required'), (20, 0.9, 'Required'), (21, 0.95, 'Required'), (60, 0.85, 'Required'), (45, 0.8, 'Preferred'), (61, 0.8, 'Preferred'), (55, 0.75, 'Required')],
    5: [(25, 0.95, 'Required'), (27, 0.9, 'Required'), (28, 0.9, 'Required'), (30, 0.9, 'Required'), (17, 0.85, 'Required'), (35, 0.85, 'Required'), (53, 0.8, 'Required'), (43, 0.7, 'Preferred')],
    6: [(1, 0.85, 'Preferred'), (30, 0.85, 'Preferred'), (32, 0.85, 'Required'), (35, 0.95, 'Required'), (17, 0.9, 'Required'), (55, 0.85, 'Required'), (57, 0.8, 'Preferred'), (39, 0.9, 'Required'), (41, 0.85, 'Required')],
    7: [(25, 0.95, 'Required'), (26, 0.85, 'Preferred'), (27, 1.0, 'Required'), (28, 0.95, 'Required'), (38, 0.8, 'Preferred'), (92, 0.75, 'Preferred'), (53, 0.7, 'Required')],
    8: [(45, 0.95, 'Required'), (46, 0.85, 'Preferred'), (44, 0.85, 'Required'), (49, 0.8, 'Required'), (89, 0.95, 'Required'), (68, 0.85, 'Required'), (50, 0.8, 'Required')],
    9: [(43, 0.95, 'Required'), (44, 0.95, 'Required'), (48, 0.95, 'Required'), (49, 0.9, 'Required'), (50, 0.9, 'Required'), (45, 0.85, 'Required'), (51, 0.8, 'Preferred'), (53, 0.85, 'Required')],
    10: [(62, 0.95, 'Required'), (65, 0.9, 'Required'), (67, 0.85, 'Required'), (70, 0.9, 'Required'), (50, 0.8, 'Required'), (66, 0.75, 'Preferred')],
    11: [(62, 0.95, 'Required'), (63, 1.0, 'Required'), (67, 0.9, 'Required'), (66, 0.95, 'Required'), (50, 0.9, 'Required'), (1, 0.75, 'Preferred')],
    12: [(1, 0.9, 'Required'), (10, 1.0, 'Required'), (43, 0.9, 'Required'), (44, 0.85, 'Required'), (48, 0.9, 'Required'), (45, 0.8, 'Preferred'), (51, 0.75, 'Preferred')],
    13: [(1, 0.95, 'Required'), (8, 1.0, 'Required'), (13, 0.95, 'Required'), (2, 0.9, 'Required'), (6, 0.9, 'Required'), (77, 0.75, 'Preferred')],
    14: [(1, 0.95, 'Required'), (7, 1.0, 'Required'), (9, 0.95, 'Required'), (12, 0.95, 'Required'), (2, 0.85, 'Required'), (6, 0.85, 'Required')],
    15: [(50, 0.95, 'Required'), (54, 1.0, 'Required'), (44, 0.9, 'Required'), (51, 0.9, 'Required'), (48, 0.85, 'Required'), (80, 0.75, 'Preferred'), (1, 0.75, 'Preferred')],
    16: [(71, 0.95, 'Required'), (72, 0.85, 'Preferred'), (25, 0.8, 'Preferred'), (75, 0.75, 'Preferred'), (76, 0.75, 'Required'), (35, 0.7, 'Required')],
    17: [(73, 1.0, 'Required'), (81, 0.85, 'Required'), (76, 0.8, 'Required'), (75, 0.75, 'Preferred'), (35, 0.7, 'Required')],
    18: [(74, 1.0, 'Required'), (76, 0.8, 'Required'), (75, 0.8, 'Preferred'), (35, 0.75, 'Required')],
    19: [(62, 0.95, 'Required'), (64, 0.9, 'Required'), (66, 0.9, 'Required'), (68, 0.9, 'Required'), (89, 0.85, 'Required'), (50, 0.8, 'Required')],
    20: [(20, 0.95, 'Required'), (60, 0.9, 'Required'), (61, 0.9, 'Required'), (17, 0.9, 'Required'), (45, 0.85, 'Required'), (89, 0.95, 'Required')],
    21: [(77, 0.95, 'Required'), (78, 0.95, 'Required'), (82, 0.95, 'Required'), (83, 0.9, 'Required'), (84, 0.9, 'Required'), (86, 0.9, 'Required')],
    22: [(78, 1.0, 'Required'), (77, 0.85, 'Preferred'), (85, 1.0, 'Required'), (82, 0.85, 'Required'), (84, 0.75, 'Preferred')],
    23: [(17, 1.0, 'Required'), (55, 0.95, 'Required'), (57, 0.85, 'Preferred'), (50, 0.8, 'Required'), (86, 0.8, 'Preferred')],
    24: [(45, 0.9, 'Required'), (68, 1.0, 'Required'), (62, 0.85, 'Required'), (49, 0.75, 'Preferred'), (44, 0.8, 'Preferred')],
    25: [(1, 0.85, 'Required'), (25, 0.8, 'Required'), (91, 1.0, 'Required'), (48, 0.8, 'Preferred'), (35, 0.8, 'Required')],
    26: [(35, 1.0, 'Required'), (36, 0.85, 'Preferred'), (99, 0.9, 'Required'), (39, 0.85, 'Required'), (32, 0.8, 'Required'), (55, 0.75, 'Required')],
    27: [(62, 0.95, 'Required'), (83, 1.0, 'Required'), (50, 0.85, 'Required'), (67, 0.85, 'Required')],
    28: [(102, 1.0, 'Required'), (79, 0.85, 'Preferred'), (64, 0.9, 'Required'), (25, 0.75, 'Preferred'), (84, 0.8, 'Preferred')],
    29: [(77, 1.0, 'Required'), (84, 0.9, 'Required'), (86, 0.9, 'Required'), (41, 0.85, 'Required')],
    30: [(94, 1.0, 'Required'), (87, 0.9, 'Required'), (18, 0.8, 'Preferred'), (35, 0.75, 'Preferred'), (88, 0.85, 'Required')],
    31: [(92, 1.0, 'Required'), (93, 0.9, 'Required'), (27, 0.85, 'Required'), (25, 0.75, 'Preferred'), (38, 0.8, 'Preferred')],
    32: [(77, 0.95, 'Required'), (1, 0.9, 'Required'), (19, 0.95, 'Required'), (84, 0.9, 'Required'), (97, 0.85, 'Required')],
    33: [(17, 0.95, 'Required'), (18, 1.0, 'Required'), (15, 0.8, 'Preferred'), (33, 0.7, 'Preferred')],
    34: [(62, 0.9, 'Required'), (95, 0.95, 'Required'), (65, 0.85, 'Required'), (87, 0.8, 'Preferred')],
    35: [(67, 0.95, 'Required'), (69, 1.0, 'Required'), (65, 0.9, 'Required'), (50, 0.85, 'Required')],
    36: [(77, 0.95, 'Required'), (1, 0.9, 'Required'), (8, 0.85, 'Required'), (85, 0.85, 'Required'), (84, 0.8, 'Required')],
    37: [(85, 0.95, 'Required'), (78, 0.9, 'Required'), (83, 0.85, 'Required'), (45, 0.8, 'Preferred'), (50, 0.8, 'Required')],
    38: [(96, 1.0, 'Required'), (48, 0.9, 'Required'), (43, 0.85, 'Required'), (66, 0.9, 'Required'), (44, 0.8, 'Required')],
    39: [(12, 1.0, 'Required'), (1, 0.95, 'Required'), (9, 0.9, 'Required'), (32, 0.85, 'Required'), (58, 0.8, 'Preferred')],
    40: [(11, 1.0, 'Required'), (58, 0.95, 'Required'), (1, 0.95, 'Required'), (2, 0.9, 'Required'), (98, 0.85, 'Preferred')]
}

with open(os.path.join(data_dir, 'career_skills.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['career_id', 'skill_id', 'importance', 'skill_type'])
    for c_id, links in career_skills_map.items():
        for skill_id, imp, s_type in links:
            writer.writerow([c_id, skill_id, imp, s_type])

print("[+] All dataset CSV files generated successfully in data/")
