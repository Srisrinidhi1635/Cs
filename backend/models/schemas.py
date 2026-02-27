from datetime import datetime


USER_ROLES = {'user', 'technician', 'admin'}
SERVICE_TYPES = {
    'electrician',
    'plumber',
    'carpenter',
    'painter',
    'cleaner',
    'masonry',
    'appliance repair',
}


def user_document(payload: dict) -> dict:
    return {
        'name': payload['name'],
        'email': payload['email'].lower(),
        'phone': payload['phone'],
        'country': payload['country'],
        'state': payload['state'],
        'password_hash': payload['password_hash'],
        'role': payload.get('role', 'user'),
        'created_at': datetime.utcnow(),
    }


def technician_document(payload: dict) -> dict:
    return {
        'name': payload['name'],
        'service_type': payload['service_type'],
        'experience': payload['experience'],
        'location': {
            'city': payload.get('city', ''),
            'coordinates': [payload['longitude'], payload['latitude']],
        },
        'contact_info': payload['contact_info'],
        'photo_url': payload.get('photo_url', ''),
        'rating': payload.get('rating', 0),
        'approved': False,
        'created_at': datetime.utcnow(),
    }


def booking_document(payload: dict) -> dict:
    return {
        'user_id': payload['user_id'],
        'technician_id': payload['technician_id'],
        'service_type': payload['service_type'],
        'issue_description': payload['issue_description'],
        'status': payload.get('status', 'requested'),
        'scheduled_for': payload.get('scheduled_for'),
        'created_at': datetime.utcnow(),
    }


def chat_document(payload: dict) -> dict:
    return {
        'user_id': payload['user_id'],
        'message': payload['message'],
        'predicted_service': payload['predicted_service'],
        'created_at': datetime.utcnow(),
    }
