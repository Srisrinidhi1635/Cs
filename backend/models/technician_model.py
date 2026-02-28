from datetime import datetime


def technician_document(data):
    return {
        "name": data["name"],
        "service_type": data["service_type"].lower(),
        "experience": int(data["experience"]),
        "location": {
            "city": data.get("city", ""),
            "lat": float(data["lat"]),
            "lng": float(data["lng"]),
        },
        "contact": data["contact"],
        "photo": data.get("photo", "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=500"),
        "rating": float(data.get("rating", 4.5)),
        "approved": False,
        "created_at": datetime.utcnow(),
    }
