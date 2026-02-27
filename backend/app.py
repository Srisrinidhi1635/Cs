from flask import Flask, jsonify
from flask_cors import CORS

from backend.config import Config
from backend.database.mongo import init_mongo
from backend.routes.admin_routes import bp as admin_bp
from backend.routes.auth_routes import bp as auth_bp
from backend.routes.booking_routes import bp as booking_bp
from backend.routes.chatbot_routes import bp as chatbot_bp
from backend.routes.technician_routes import bp as technician_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    init_mongo(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(technician_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(admin_bp)

    @app.get('/api/health')
    def health_check():
        return jsonify({'status': 'ok'})

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
