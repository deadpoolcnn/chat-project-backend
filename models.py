from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    public_key = db.Column(db.Text, nullable=False)

class Message(db.Model):
    msg_id = db.Column(db.String(64), primary_key=True)
    from_user = db.Column(db.String(64), db.ForeignKey('user.user_id'))
    to_user = db.Column(db.String(64), db.ForeignKey('user.user_id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    encrypted_key = db.Column(db.Text)
    iv = db.Column(db.Text)
    ciphertext = db.Column(db.Text)
    signature = db.Column(db.Text)
