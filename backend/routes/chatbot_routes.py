from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.chatbot_controller import analyze_issue


chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api/chatbot")

chatbot_bp.post("/analyze")(jwt_required()(analyze_issue))
