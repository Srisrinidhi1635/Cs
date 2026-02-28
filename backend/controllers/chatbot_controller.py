from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from database.db import chat_history_collection
from models.chat_model import chat_document
from utils.nlp import classify_service


def analyze_issue():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    result = classify_service(message)
    chat_history_collection.insert_one(chat_document(user_id, message, result))

    return jsonify({
        "classification": result,
        "reply": (
            f"It sounds like you need a {result['service_type']}. "
            "I can now show nearby technicians for this service."
        )
    })
