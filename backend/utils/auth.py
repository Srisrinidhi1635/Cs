from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)


def create_token(user_id: str, role: str):
    expires_at = datetime.now(tz=timezone.utc) + timedelta(hours=current_app.config['JWT_EXP_HOURS'])
    payload = {'sub': user_id, 'role': role, 'exp': expires_at}
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')


def decode_token(token: str):
    return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])


def jwt_required(roles=None):
    roles = roles or []

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            header = request.headers.get('Authorization', '')
            if not header.startswith('Bearer '):
                return jsonify({'error': 'Missing bearer token'}), 401
            token = header.split(' ', maxsplit=1)[1]
            try:
                payload = decode_token(token)
            except Exception:
                return jsonify({'error': 'Invalid or expired token'}), 401
            request.user = payload
            if roles and payload.get('role') not in roles:
                return jsonify({'error': 'Forbidden'}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
