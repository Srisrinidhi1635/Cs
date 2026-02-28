from flask import jsonify
from flask_jwt_extended import get_jwt

from database.db import users_collection, technicians_collection, bookings_collection
from utils.helpers import serialize_mongo_doc


def admin_dashboard():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    users = [serialize_mongo_doc(u) for u in users_collection.find({}, {"password": 0})]
    technicians = [serialize_mongo_doc(t) for t in technicians_collection.find()]
    bookings = [serialize_mongo_doc(b) for b in bookings_collection.find()]

    return jsonify({
        "counts": {
            "users": len(users),
            "technicians": len(technicians),
            "bookings": len(bookings),
        },
        "users": users,
        "technicians": technicians,
        "bookings": bookings,
    })
