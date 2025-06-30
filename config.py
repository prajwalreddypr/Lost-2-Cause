import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32).hex())
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.urandom(32).hex())
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)  # 1 week expiration
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_CSRF_IN_COOKIES = False  # Disable if not using CSRF protection
    
    # Database
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', 'sqlite:///site.db')
        .replace('postgres://', 'postgresql://', 1)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS
    CORS_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')