from pymongo import MongoClient
from config import Config


client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]


users_collection = db["users"]
technicians_collection = db["technicians"]
bookings_collection = db["bookings"]
chat_history_collection = db["chat_history"]


# Useful indexes for production-like behavior
users_collection.create_index("email", unique=True)
technicians_collection.create_index([("service_type", 1), ("approved", 1)])
technicians_collection.create_index([("location.lat", 1), ("location.lng", 1)])
bookings_collection.create_index([("user_id", 1), ("status", 1)])
bookings_collection.create_index([("technician_id", 1), ("status", 1)])
