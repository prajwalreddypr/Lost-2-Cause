import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Handle Railway's PostgreSQL URL format
    if 'DATABASE_URL' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://', 1)
    
    # Enhanced CORS configuration
    CORS(
        app,
        resources={
            r"/auth/*": {"origins": os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')},
            r"/user": {"origins": os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')}
        },
        supports_credentials=True,
        expose_headers=['Content-Type', 'Set-Cookie'],
        allow_headers=['Content-Type', 'Authorization']
    )
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Create tables if not exists
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Add security headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('X-Content-Type-Options', 'nosniff')
        return response

    return app