from flask import Blueprint, request, jsonify
# from models import db, Message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/send_message', methods=['POST'])
def send_message():
    # 处理加密消息发送
    return jsonify({'msg': 'send_message endpoint'})

@messages_bp.route('/get_messages', methods=['GET'])
def get_messages():
    # 获取消息记录（密文）
    return jsonify({'msg': 'get_messages endpoint'})
