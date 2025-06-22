from flask import Blueprint, request, jsonify
from models import db, User
from sqlalchemy import and_

class Friend(db.Model):
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.user_id'))
    friend_id = db.Column(db.String(64), db.ForeignKey('user.user_id'))

friends_bp = Blueprint('friends', __name__)

@friends_bp.route('/friends', methods=['GET', 'POST', 'DELETE'])
def manage_friends():
    try:
        if request.method == 'GET':
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            if not user:
                return jsonify({'message': '用户不存在', 'data': []}), 404
            # 查询当前用户的所有好友
            friend_links = Friend.query.filter_by(user_id=user.user_id).all()
            friends = []
            for link in friend_links:
                friend_user = User.query.filter_by(user_id=link.friend_id).first()
                if friend_user:
                    friends.append({'user_id': friend_user.user_id, 'username': friend_user.username, 'publicKey': friend_user.public_key})
            return jsonify({'message': '查询成功', 'data': friends}), 200
        elif request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            friendName = data.get('friendName')
            if not username or not friendName:
                return jsonify({'message': '缺少必要参数', 'data': []}), 200
            user = User.query.filter_by(username=username).first()
            friend = User.query.filter_by(username=friendName).first()
            if not user or not friend:
                return jsonify({'message': '用户或好友用户不存在', 'data': []}), 404
            # 检查是否已是好友
            exists = Friend.query.filter(and_(Friend.user_id==user.user_id, Friend.friend_id==friend.user_id)).first()
            if exists:
                return jsonify({'message': '已添加为好友', 'data': []}), 200
            # 添加好友关系（双向）
            new_friend = Friend(user_id=user.user_id, friend_id=friend.user_id)
            new_friend_reverse = Friend(user_id=friend.user_id, friend_id=user.user_id)
            db.session.add(new_friend)
            db.session.add(new_friend_reverse)
            db.session.commit()
            friend_data = {'user_id': friend.user_id, 'username': friend.username, 'publicKey': friend.public_key}
            return jsonify({'message': f'添加好友 {friendName} 成功', 'data': [friend_data]}), 201
        elif request.method == 'DELETE':
            data = request.get_json()
            username = data.get('username')
            friendName = data.get('friendName')
            if not username or not friendName:
                return jsonify({'message': '缺少必要参数', 'data': []}), 400
            user = User.query.filter_by(username=username).first()
            friend = User.query.filter_by(username=friendName).first()
            if not user or not friend:
                return jsonify({'message': '用户或好友用户不存在', 'data': []}), 404
            link = Friend.query.filter(and_(Friend.user_id==user.user_id, Friend.friend_id==friend.user_id)).first()
            if not link:
                return jsonify({'message': '好友关系不存在', 'data': []}), 404
            db.session.delete(link)
            db.session.commit()
            return jsonify({'message': f'删除好友 {friendName} 成功', 'data': []}), 200
    except Exception as e:
        return jsonify({'message': '操作失败', 'data': [], 'error': str(e)}), 500
