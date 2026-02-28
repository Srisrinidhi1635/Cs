from datetime import datetime


def booking_document(data, user_id):
    return {
        "user_id": user_id,
        "technician_id": data["technician_id"],
        "service_type": data["service_type"].lower(),
        "issue_description": data["issue_description"],
        "scheduled_at": data.get("scheduled_at"),
        "status": "requested",
        "created_at": datetime.utcnow(),
    }
