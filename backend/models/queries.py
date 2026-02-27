from bson import ObjectId

from backend.database.mongo import mongo


class UserModel:
    collection = 'users'

    @staticmethod
    def create(doc: dict):
        return mongo.db[UserModel.collection].insert_one(doc)

    @staticmethod
    def find_by_email(email: str):
        return mongo.db[UserModel.collection].find_one({'email': email.lower()})

    @staticmethod
    def get_all():
        return list(mongo.db[UserModel.collection].find({}, {'password_hash': 0}))


class TechnicianModel:
    collection = 'technicians'

    @staticmethod
    def create(doc: dict):
        return mongo.db[TechnicianModel.collection].insert_one(doc)

    @staticmethod
    def find_approved(service_type: str):
        return list(
            mongo.db[TechnicianModel.collection].find(
                {'service_type': service_type, 'approved': True}
            )
        )

    @staticmethod
    def get_all():
        return list(mongo.db[TechnicianModel.collection].find())

    @staticmethod
    def set_approval(tech_id: str, approved: bool):
        return mongo.db[TechnicianModel.collection].update_one(
            {'_id': ObjectId(tech_id)}, {'$set': {'approved': approved}}
        )


class BookingModel:
    collection = 'bookings'

    @staticmethod
    def create(doc: dict):
        return mongo.db[BookingModel.collection].insert_one(doc)

    @staticmethod
    def by_user(user_id: str):
        return list(mongo.db[BookingModel.collection].find({'user_id': user_id}))

    @staticmethod
    def cancel(booking_id: str, user_id: str):
        return mongo.db[BookingModel.collection].update_one(
            {'_id': ObjectId(booking_id), 'user_id': user_id},
            {'$set': {'status': 'cancelled'}},
        )

    @staticmethod
    def get_all():
        return list(mongo.db[BookingModel.collection].find())


class ChatModel:
    collection = 'chat_history'

    @staticmethod
    def create(doc: dict):
        return mongo.db[ChatModel.collection].insert_one(doc)
