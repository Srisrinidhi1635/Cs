from flask import Blueprint

from backend.controllers.auth_controller import login_user, register_user

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

bp.post('/register')(register_user)
bp.post('/login')(login_user)
