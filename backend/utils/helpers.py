from bson import ObjectId


def serialize_mongo_doc(document):
    if not document:
        return None

    doc = dict(document)
    doc["_id"] = str(doc["_id"])
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc
