from flask import request, jsonify, g
from functools import wraps
import time
import jwt
from app.config import SECRET_KEY, RATE_LIMIT_WINDOW, RATE_LIMIT_MAX_REQUESTS

tokens = {}
rate_limits = {}

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': time.time() + 3600  # token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    tokens[user_id] = token
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            g.user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

def rate_limited(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = g.user_id
        current_time = time.time()
        if user_id not in rate_limits:
            rate_limits[user_id] = []
        rate_limits[user_id] = [t for t in rate_limits[user_id] if current_time - t < RATE_LIMIT_WINDOW]
        if len(rate_limits[user_id]) >= RATE_LIMIT_MAX_REQUESTS:
            return jsonify({'message': 'Rate limit exceeded!'}), 429
        rate_limits[user_id].append(current_time)
        return f(*args, **kwargs)
    return decorated
