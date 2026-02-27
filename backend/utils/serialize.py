from datetime import datetime


def normalize_mongo(doc):
    if doc is None:
        return None
    out = {}
    for key, value in doc.items():
        if key == '_id':
            out['id'] = str(value)
        elif isinstance(value, datetime):
            out[key] = value.isoformat()
        else:
            out[key] = value
    return out


def normalize_many(docs):
    return [normalize_mongo(doc) for doc in docs]
