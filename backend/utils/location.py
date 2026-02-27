from math import asin, cos, radians, sin, sqrt


def haversine_km(lat1, lon1, lat2, lon2):
    radius = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * radius * asin(sqrt(a))


def rank_nearest(user_lat: float, user_lon: float, technicians: list[dict]):
    ranked = []
    for tech in technicians:
        lon, lat = tech.get('location', {}).get('coordinates', [None, None])
        if lat is None or lon is None:
            continue
        distance = haversine_km(user_lat, user_lon, lat, lon)
        ranked.append({**tech, 'distance_km': round(distance, 2)})
    return sorted(ranked, key=lambda item: item['distance_km'])
