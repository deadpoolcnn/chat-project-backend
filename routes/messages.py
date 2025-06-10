from flask import Blueprint, request, jsonify
from models import db, Message, User
import uuid
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        from_user = data.get('from_user')
        to_user = data.get('to_user')
        ciphertext = data.get('ciphertext')
        encrypted_key = data.get('encrypted_key')
        iv = data.get('iv')
        signature = data.get('signature')
        if not all([from_user, to_user, ciphertext, encrypted_key, iv, signature]):
            return jsonify({'message': '缺少必要参数', 'data': []}), 400
        # 检查用户是否存在
        sender = User.query.filter_by(username=from_user).first()
        receiver = User.query.filter_by(username=to_user).first()
        if not sender or not receiver:
            return jsonify({'message': '发送方或接收方不存在', 'data': []}), 404
        msg = Message(
            msg_id=str(uuid.uuid4()),
            from_user=from_user,  # 存用户名
            to_user=to_user,      # 存用户名
            timestamp=datetime.utcnow(),
            encrypted_key=encrypted_key,
            iv=iv,
            ciphertext=ciphertext,
            signature=signature
        )
        db.session.add(msg)
        db.session.commit()
        return jsonify({'message': '消息发送成功', 'data': []}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '消息发送失败', 'data': [], 'error': str(e)}), 500

@messages_bp.route('/get_messages', methods=['GET'])
def get_messages():
    try:
        from_user = request.args.get('from_user')
        to_user = request.args.get('to_user')
        if not from_user or not to_user:
            return jsonify({'message': '缺少必要参数', 'data': []}), 400
        # 直接用用户名查找
        messages = Message.query.filter(
            ((Message.from_user == from_user) & (Message.to_user == to_user)) |
            ((Message.from_user == to_user) & (Message.to_user == from_user))
        ).order_by(Message.timestamp.asc()).all()
        data = [
            {
                'msg_id': m.msg_id,
                'from_user': m.from_user,  # 返回用户名
                'to_user': m.to_user,      # 返回用户名
                'timestamp': m.timestamp.isoformat(),
                'encrypted_key': m.encrypted_key,
                'iv': m.iv,
                'ciphertext': m.ciphertext,
                'signature': m.signature
            } for m in messages
        ]
        return jsonify({'message': '查询成功', 'data': data}), 200
    except Exception as e:
        return jsonify({'message': '查询失败', 'data': [], 'error': str(e)}), 500
