from flask import jsonify, request

from backend.models.queries import UserModel
from backend.models.schemas import user_document
from backend.utils.auth import create_token, hash_password, verify_password
from backend.utils.serialize import normalize_mongo


def register_user():
    payload = request.get_json(force=True)
    required = ['name', 'email', 'phone', 'country', 'state', 'password']
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    if UserModel.find_by_email(payload['email']):
        return jsonify({'error': 'Email already registered'}), 409

    doc = user_document(
        {
            **payload,
            'password_hash': hash_password(payload['password']),
            'role': payload.get('role', 'user'),
        }
    )
    inserted = UserModel.create(doc)
    token = create_token(str(inserted.inserted_id), doc['role'])
    return jsonify({'token': token, 'user': normalize_mongo({**doc, '_id': inserted.inserted_id})}), 201


def login_user():
    payload = request.get_json(force=True)
    email = payload.get('email', '').lower()
    password = payload.get('password', '')

    user = UserModel.find_by_email(email)
    if not user or not verify_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(str(user['_id']), user['role'])
    return jsonify({'token': token, 'user': normalize_mongo({k: v for k, v in user.items() if k != 'password_hash'})})
