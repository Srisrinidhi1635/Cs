from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.booking_controller import create_booking, list_bookings, cancel_booking


booking_bp = Blueprint("bookings", __name__, url_prefix="/api/bookings")

booking_bp.post("")(jwt_required()(create_booking))
booking_bp.get("")(jwt_required()(list_bookings))
booking_bp.delete("/<booking_id>")(jwt_required()(cancel_booking))
