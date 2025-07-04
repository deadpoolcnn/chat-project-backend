from flask import Blueprint, request, jsonify
from models import db, User
import uuid
from utils.crypto import generate_rsa_keypair

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        public_key = data.get('public_key')

        if not username or not password or not public_key:
            return jsonify({'msg': 'Missing required parameters'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'msg': 'Username already exists'}), 409

        user = User(user_id=str(uuid.uuid4()), username=username, password=password, public_key=public_key)
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': 'Registration successful', 'public_key': public_key}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Registration failed', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'msg': 'Missing required parameters'}), 400

        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return jsonify({'msg': 'Invalid username or password'}), 401

        return jsonify({'msg': 'Login successful', 'user_id': user.user_id}), 200
    except Exception as e:
        return jsonify({'msg': 'Login failed', 'error': str(e)}), 500

@auth_bp.route('/getPublicKey', methods=['GET'])
def get_public_key():
    username = request.args.get('username')
    if not username:
        return jsonify({'msg': 'Missing required parameters'}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify({'msg': 'Query successful', 'public_key': user.public_key}), 200
