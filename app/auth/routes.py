from flask import Blueprint, request, jsonify
from app.auth.models import User
from app import db, bcrypt
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'All fields are required'}), 400
    
    # Validate password match
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Passwords do not match'}), 400
    
    # Validate email uniqueness
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    # Create user
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
            'first_name': user.first_name,
            'last_name': user.last_name,
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
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        }), 200
    return jsonify({'message': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/user', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email
        }), 200
    return jsonify({'message': 'Not logged in'}), 401