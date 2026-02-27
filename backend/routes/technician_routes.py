from flask import Blueprint

from backend.controllers.technician_controller import (
    approve_technician,
    list_technicians,
    register_technician,
    reject_technician,
)

bp = Blueprint('technicians', __name__, url_prefix='/api/technicians')

bp.post('')(register_technician)
bp.get('')(list_technicians)
bp.patch('/<tech_id>/approve')(approve_technician)
bp.patch('/<tech_id>/reject')(reject_technician)
