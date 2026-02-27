from flask import Blueprint

from backend.controllers.booking_controller import (
    cancel_booking,
    create_booking,
    list_all_bookings,
    list_my_bookings,
)

bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

bp.post('')(create_booking)
bp.get('/me')(list_my_bookings)
bp.patch('/<booking_id>/cancel')(cancel_booking)
bp.get('')(list_all_bookings)
