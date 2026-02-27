from flask import Blueprint

from backend.controllers.admin_controller import dashboard_summary

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

bp.get('/dashboard')(dashboard_summary)
