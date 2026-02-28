from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import get_jwt

from database.db import technicians_collection
from models.technician_model import technician_document
from utils.helpers import serialize_mongo_doc
from utils.location import haversine_distance_km


def register_technician():
    data = request.get_json() or {}
    required = ["name", "service_type", "experience", "lat", "lng", "contact"]
    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    doc = technician_document(data)
    inserted = technicians_collection.insert_one(doc)
    return jsonify({
        "message": "Technician registered. Awaiting admin approval.",
        "technician": serialize_mongo_doc(technicians_collection.find_one({"_id": inserted.inserted_id}))
    }), 201


def list_technicians():
    service_type = request.args.get("service_type")
    user_lat = request.args.get("lat", type=float)
    user_lng = request.args.get("lng", type=float)

    query = {"approved": True}
    if service_type:
        query["service_type"] = service_type.lower()

    technicians = [serialize_mongo_doc(t) for t in technicians_collection.find(query)]

    if user_lat is not None and user_lng is not None:
        for tech in technicians:
            tech["distance_km"] = haversine_distance_km(
                user_lat, user_lng, tech["location"]["lat"], tech["location"]["lng"]
            )
        technicians.sort(key=lambda x: x.get("distance_km", 99999))

    return jsonify(technicians)


def approve_technician(tech_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    payload = request.get_json() or {}
    approved = bool(payload.get("approved", True))
    updated = technicians_collection.find_one_and_update(
        {"_id": ObjectId(tech_id)},
        {"$set": {"approved": approved}},
        return_document=True,
    )
    if not updated:
        return jsonify({"error": "Technician not found"}), 404

    return jsonify({"message": "Technician status updated", "technician": serialize_mongo_doc(updated)})
