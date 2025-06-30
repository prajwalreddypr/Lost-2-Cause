from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
from app.auth.models import User
from app import db, bcrypt
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'All fields are required'}), 400
    
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Passwords do not match'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Registration successful',
        'user': {
            'id': user.id,
            'email': user.email
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.verify_password(password):
        access_token = create_access_token(
            identity=user.id,
            expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES
        )
        
        response = jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email
            }
        })
        
        set_access_cookies(response, access_token)
        return response, 200
    
    return jsonify({'message': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }), 200