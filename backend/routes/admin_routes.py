from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.admin_controller import admin_dashboard


admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

admin_bp.get("/dashboard")(jwt_required()(admin_dashboard))
