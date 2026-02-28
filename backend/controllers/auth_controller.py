from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import users_collection
from models.user_model import user_document
from utils.helpers import serialize_mongo_doc


def register_user():
    data = request.get_json() or {}
    required = ["name", "email", "phone", "country", "state", "password"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if users_collection.find_one({"email": data["email"].lower().strip()}):
        return jsonify({"error": "Email already exists"}), 409

    hashed = generate_password_hash(data["password"])
    role = data.get("role", "user")
    doc = user_document(data, hashed, role=role)
    inserted = users_collection.insert_one(doc)
    token = create_access_token(identity=str(inserted.inserted_id), additional_claims={"role": role})

    return jsonify({
        "message": "Registered successfully",
        "token": token,
        "user": serialize_mongo_doc(users_collection.find_one({"_id": inserted.inserted_id}, {"password": 0}))
    }), 201


def login_user():
    data = request.get_json() or {}
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")

    user = users_collection.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["_id"]), additional_claims={"role": user.get("role", "user")})
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": serialize_mongo_doc({k: v for k, v in user.items() if k != "password"})
    })
