from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.technician_controller import register_technician, list_technicians, approve_technician


technician_bp = Blueprint("technicians", __name__, url_prefix="/api/technicians")

technician_bp.post("")(register_technician)
technician_bp.get("")(list_technicians)
technician_bp.patch("/<tech_id>/approve")(jwt_required()(approve_technician))
