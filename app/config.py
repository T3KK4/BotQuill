import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Set up of secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Using SQLite for Local Development with no tracking
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB Max file upload
    