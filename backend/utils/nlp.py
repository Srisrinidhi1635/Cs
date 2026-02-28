import re

SERVICE_KEYWORDS = {
    "plumber": ["sink", "pipe", "leak", "drain", "tap", "toilet", "water"],
    "electrician": ["light", "electric", "switch", "socket", "wire", "fan", "power"],
    "carpenter": ["wood", "door", "window", "furniture", "cabinet", "table"],
    "painter": ["paint", "wall", "color", "stain", "coating"],
    "cleaner": ["clean", "dust", "sanitize", "mop", "deep cleaning"],
    "masonry": ["brick", "cement", "concrete", "tile", "plaster", "wall crack"],
    "appliance repair": ["washing machine", "refrigerator", "ac", "microwave", "oven", "appliance"],
}


def classify_service(text):
    message = text.lower().strip()

    score = {service: 0 for service in SERVICE_KEYWORDS}
    for service, keywords in SERVICE_KEYWORDS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", message):
                score[service] += 1

    best = max(score, key=score.get)
    if score[best] == 0:
        return {
            "service_type": "cleaner",
            "confidence": 0.35,
            "reason": "No strong keyword match; defaulted to cleaner/general support.",
        }

    confidence = min(0.99, 0.5 + (score[best] * 0.15))
    return {
        "service_type": best,
        "confidence": round(confidence, 2),
        "reason": f"Matched keywords for {best}",
    }
