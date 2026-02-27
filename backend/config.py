import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
    JWT_SECRET = os.getenv('JWT_SECRET', 'change-jwt-secret')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_home_service')
    JWT_EXP_HOURS = int(os.getenv('JWT_EXP_HOURS', '24'))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
