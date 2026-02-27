// MongoDB schema/index bootstrap script for Smart Home Service Assistant

db = db.getSiblingDB('smart_home_service')

db.users.createIndex({ email: 1 }, { unique: true })
db.technicians.createIndex({ 'location.coordinates': '2dsphere' })
db.bookings.createIndex({ user_id: 1, created_at: -1 })
db.chat_history.createIndex({ user_id: 1, created_at: -1 })
