from flask import jsonify, request

from backend.models.queries import BookingModel
from backend.models.schemas import booking_document
from backend.utils.auth import jwt_required
from backend.utils.serialize import normalize_many, normalize_mongo


@jwt_required()
def create_booking():
    payload = request.get_json(force=True)
    required = ['technician_id', 'service_type', 'issue_description']
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    doc = booking_document(
        {
            **payload,
            'user_id': request.user['sub'],
            'status': 'requested',
        }
    )
    inserted = BookingModel.create(doc)
    return jsonify(normalize_mongo({**doc, '_id': inserted.inserted_id})), 201


@jwt_required()
def list_my_bookings():
    return jsonify(normalize_many(BookingModel.by_user(request.user['sub'])))


@jwt_required()
def cancel_booking(booking_id: str):
    result = BookingModel.cancel(booking_id, request.user['sub'])
    if not result.modified_count:
        return jsonify({'error': 'Booking not found'}), 404
    return jsonify({'message': 'Booking cancelled'})


@jwt_required(roles=['admin'])
def list_all_bookings():
    return jsonify(normalize_many(BookingModel.get_all()))
