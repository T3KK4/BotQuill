import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Set up of secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cynthia$700$'
    
    # Using SQLite for Local Development with no tracking
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///botcynthia.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB Max file upload
    
    # Writer seed credentials (only used for initial setup)
    WRITER_USERNAME = os.environ.get('WRITER_USERNAME')
    WRITER_EMAIL = os.environ.get('WRITER_EMAIL')
    WRITER_PASSWORD = os.environ.get('WRITER_PASSWORD')
    DEFAULT_MESSAGE = os.environ.get('DEFAULT_MESSAGE', 'Welcome to BotQuill.')
    