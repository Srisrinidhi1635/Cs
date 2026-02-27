from pymongo import MongoClient


class Mongo:
    client: MongoClient | None = None
    db = None


mongo = Mongo()


def init_mongo(app):
    mongo.client = MongoClient(app.config['MONGO_URI'])
    db_name = app.config['MONGO_URI'].rsplit('/', maxsplit=1)[-1]
    mongo.db = mongo.client[db_name]
    return mongo.db
