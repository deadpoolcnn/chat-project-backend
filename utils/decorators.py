# 认证/权限相关装饰器
from functools import wraps
from flask import request, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查会话令牌
        return f(*args, **kwargs)
    return decorated_function
