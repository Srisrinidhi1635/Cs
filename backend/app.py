from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from config import Config
from routes.auth_routes import auth_bp
from routes.technician_routes import technician_bp
from routes.booking_routes import booking_bp
from routes.chatbot_routes import chatbot_bp
from routes.admin_routes import admin_bp


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(technician_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(admin_bp)

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok", "service": "Smart Home Service Assistant API"})

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, port=5000)
