from datetime import datetime


def chat_document(user_id, message, classification):
    return {
        "user_id": user_id,
        "message": message,
        "classification": classification,
        "created_at": datetime.utcnow(),
    }
