import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ai-career-recommender-secret-key-12345')
    DEBUG = True
    
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'ai_career_recommender')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    
    # Upload folder for dynamic graphs or visualization assets
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'static', 'images'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

    # Hybrid Recommendation Engine Configuration
    ML_WEIGHT = float(os.environ.get('ML_WEIGHT', 0.40))
    GNN_WEIGHT = float(os.environ.get('GNN_WEIGHT', 0.60))
    DIVERSITY_PENALTY = float(os.environ.get('DIVERSITY_PENALTY', 0.15))
    TOP_K_RECOMMENDATIONS = int(os.environ.get('TOP_K_RECOMMENDATIONS', 5))
    MAX_SAME_CATEGORY_LIMIT = int(os.environ.get('MAX_SAME_CATEGORY_LIMIT', 2))
