from flask import Blueprint

from backend.controllers.chatbot_controller import chatbot_match

bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

bp.post('/match')(chatbot_match)
