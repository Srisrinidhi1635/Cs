from flask import jsonify, request

from backend.models.queries import TechnicianModel
from backend.models.schemas import SERVICE_TYPES, technician_document
from backend.utils.auth import jwt_required
from backend.utils.serialize import normalize_many, normalize_mongo


@jwt_required()
def register_technician():
    payload = request.get_json(force=True)
    required = ['name', 'service_type', 'experience', 'latitude', 'longitude', 'contact_info']
    missing = [field for field in required if payload.get(field) in (None, '')]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400
    if payload['service_type'] not in SERVICE_TYPES:
        return jsonify({'error': 'Unsupported service type'}), 400

    doc = technician_document(
        {
            **payload,
            'latitude': float(payload['latitude']),
            'longitude': float(payload['longitude']),
        }
    )
    inserted = TechnicianModel.create(doc)
    return jsonify(normalize_mongo({**doc, '_id': inserted.inserted_id})), 201


@jwt_required(roles=['admin'])
def list_technicians():
    return jsonify(normalize_many(TechnicianModel.get_all()))


@jwt_required(roles=['admin'])
def approve_technician(tech_id: str):
    TechnicianModel.set_approval(tech_id, True)
    return jsonify({'message': 'Technician approved'})


@jwt_required(roles=['admin'])
def reject_technician(tech_id: str):
    TechnicianModel.set_approval(tech_id, False)
    return jsonify({'message': 'Technician rejected'})
