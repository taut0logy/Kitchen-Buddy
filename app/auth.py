from flask import request, jsonify, g
from functools import wraps
import time
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, RATE_LIMIT_WINDOW, RATE_LIMIT_MAX_REQUESTS

tokens = {}
rate_limits = {}

tokens_blacklist = set()
refresh_tokens = {}

def generate_token(user_id):
    # Access token - expires in 1 hour
    access_token_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    
    # Refresh token - expires in 7 days
    refresh_token_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    
    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm='HS256')
    
    refresh_tokens[user_id] = refresh_token
    return {'access_token': access_token, 'refresh_token': refresh_token}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(" ")[1]
            
            # Check if token is blacklisted
            if token in tokens_blacklist:
                return jsonify({'message': 'Token has been revoked!'}), 401
                
            # Decode token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            # Verify token type
            if payload['type'] != 'access':
                return jsonify({'message': 'Invalid token type!'}), 401
                
            g.user_id = payload['user_id']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
            
        return f(*args, **kwargs)
    return decorated

def refresh_access_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        
        if payload['type'] != 'refresh':
            return jsonify({'message': 'Invalid token type!'}), 401
            
        if refresh_tokens.get(user_id) != refresh_token:
            return jsonify({'message': 'Invalid refresh token!'}), 401
            
        new_access_token = generate_token(user_id)['access_token']
        return jsonify({'access_token': new_access_token})
        
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token!'}), 401

def revoke_token(token):
    tokens_blacklist.add(token)

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
