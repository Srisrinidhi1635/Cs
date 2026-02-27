from flask import jsonify, request

from backend.models.queries import ChatModel, TechnicianModel
from backend.models.schemas import chat_document
from backend.utils.auth import jwt_required
from backend.utils.location import rank_nearest
from backend.utils.nlp import classify_service
from backend.utils.serialize import normalize_many


@jwt_required()
def chatbot_match():
    payload = request.get_json(force=True)
    text = payload.get('message', '').strip()
    lat = payload.get('latitude')
    lon = payload.get('longitude')
    if not text:
        return jsonify({'error': 'Message is required'}), 400
    if lat is None or lon is None:
        return jsonify({'error': 'latitude and longitude are required'}), 400

    service_type = classify_service(text)
    history_doc = chat_document(
        {
            'user_id': request.user['sub'],
            'message': text,
            'predicted_service': service_type,
        }
    )
    ChatModel.create(history_doc)

    technicians = TechnicianModel.find_approved(service_type)
    nearest = rank_nearest(float(lat), float(lon), technicians)

    return jsonify(
        {
            'predicted_service': service_type,
            'technicians': normalize_many(nearest[:10]),
        }
    )
