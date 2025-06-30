import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Handle PostgreSQL URL format
    if 'DATABASE_URL' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://', 1)
    
    # Configure CORS
    CORS(
        app,
        resources={r"/*": {"origins": app.config['CORS_ORIGINS']}},
        supports_credentials=True,
        expose_headers=['Content-Type'],
        allow_headers=['Content-Type', 'Authorization']
    )
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The token has expired",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "Invalid token",
            "error": "invalid_token"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "Missing access token",
            "error": "authorization_required"
        }), 401

    return app