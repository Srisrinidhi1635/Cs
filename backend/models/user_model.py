from datetime import datetime


def user_document(data, password_hash, role="user"):
    return {
        "name": data["name"],
        "email": data["email"].lower().strip(),
        "phone": data["phone"],
        "country": data["country"],
        "state": data["state"],
        "password": password_hash,
        "role": role,
        "created_at": datetime.utcnow(),
    }
