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
            return jsonify({'msg': '缺少必要参数'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'msg': '用户名已存在'}), 409

        user = User(user_id=str(uuid.uuid4()), username=username, password=password, public_key=public_key)
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg': '注册成功', 'public_key': public_key}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': '注册失败', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'msg': '缺少必要参数'}), 400

        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return jsonify({'msg': '用户名或密码错误'}), 401

        return jsonify({'msg': '登录成功', 'user_id': user.user_id}), 200
    except Exception as e:
        return jsonify({'msg': '登录失败', 'error': str(e)}), 500
