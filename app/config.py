import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + str(BASE_DIR / 'plano_de_aula.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True
    }
    
    # Upload settings
    UPLOAD_FOLDER = BASE_DIR / os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 32 * 1024 * 1024))  # 32MB max
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Admin settings
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_INITIAL_PASSWORD = os.getenv('ADMIN_INITIAL_PASSWORD')
    ADMIN_NAME = os.getenv('ADMIN_NAME', 'Administrador')

