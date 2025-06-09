from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.friends import friends_bp
from routes.messages import messages_bp
from database import db
from models import *

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True) # 支持携带cookie等认证信息
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(friends_bp)
app.register_blueprint(messages_bp)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Flask加密聊天系统已启动，详见API文档。'

if __name__ == '__main__':
    app.run(debug=True)
