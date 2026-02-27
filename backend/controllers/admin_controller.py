from flask import jsonify

from backend.models.queries import BookingModel, TechnicianModel, UserModel
from backend.utils.auth import jwt_required
from backend.utils.serialize import normalize_many


@jwt_required(roles=['admin'])
def dashboard_summary():
    users = UserModel.get_all()
    technicians = TechnicianModel.get_all()
    bookings = BookingModel.get_all()
    return jsonify(
        {
            'counts': {
                'users': len(users),
                'technicians': len(technicians),
                'bookings': len(bookings),
            },
            'users': normalize_many(users),
            'technicians': normalize_many(technicians),
            'bookings': normalize_many(bookings),
        }
    )
