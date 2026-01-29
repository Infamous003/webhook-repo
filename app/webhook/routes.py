from flask import Blueprint, jsonify, request, current_app
from app.webhook.services import build_push_event

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if not request.is_json:
        return jsonify({"error": "Invalid payload format"}), 400
    
    event = request.headers.get("X-GitHub-Event")
    payload = request.get_json()

    if event == "push":
        data = build_push_event(payload=payload)

        current_app.events_collection.insert_one(data)
        
    return jsonify({"status": "ok"}), 200
