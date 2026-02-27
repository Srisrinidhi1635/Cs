SERVICE_KEYWORDS = {
    'electrician': ['light', 'wiring', 'switch', 'power', 'socket', 'fan'],
    'plumber': ['sink', 'leak', 'pipe', 'toilet', 'drain', 'tap'],
    'carpenter': ['wood', 'door', 'furniture', 'cabinet', 'table'],
    'painter': ['paint', 'wall', 'coating', 'color', 'primer'],
    'cleaner': ['clean', 'dust', 'sanitize', 'mop', 'vacuum'],
    'masonry': ['cement', 'brick', 'plaster', 'tile', 'floor crack'],
    'appliance repair': ['refrigerator', 'washing machine', 'ac', 'microwave', 'appliance'],
}


def classify_service(text: str) -> str:
    lowered = text.lower()
    scores = {
        service: sum(1 for word in keywords if word in lowered)
        for service, keywords in SERVICE_KEYWORDS.items()
    }
    service, score = max(scores.items(), key=lambda item: item[1])
    return service if score > 0 else 'cleaner'
