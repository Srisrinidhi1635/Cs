from flask import Blueprint
from controllers.auth_controller import register_user, login_user


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

auth_bp.post("/register")(register_user)
auth_bp.post("/login")(login_user)
