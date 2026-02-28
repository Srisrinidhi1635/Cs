from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from database.db import bookings_collection, technicians_collection
from models.booking_model import booking_document
from utils.helpers import serialize_mongo_doc


def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    required = ["technician_id", "service_type", "issue_description"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    tech = technicians_collection.find_one({"_id": ObjectId(data["technician_id"]), "approved": True})
    if not tech:
        return jsonify({"error": "Technician unavailable"}), 404

    doc = booking_document(data, user_id)
    inserted = bookings_collection.insert_one(doc)
    return jsonify({
        "message": "Booking requested successfully",
        "booking": serialize_mongo_doc(bookings_collection.find_one({"_id": inserted.inserted_id}))
    }), 201


def list_bookings():
    user_id = get_jwt_identity()
    bookings = [serialize_mongo_doc(b) for b in bookings_collection.find({"user_id": user_id})]
    return jsonify(bookings)


def cancel_booking(booking_id):
    user_id = get_jwt_identity()
    booking = bookings_collection.find_one_and_update(
        {"_id": ObjectId(booking_id), "user_id": user_id},
        {"$set": {"status": "cancelled"}},
        return_document=True,
    )
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": "Booking cancelled", "booking": serialize_mongo_doc(booking)})
