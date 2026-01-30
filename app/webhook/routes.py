from flask import Blueprint, jsonify, request, current_app
from app.webhook.services import build_push_event, build_pull_request_event

webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if not request.is_json:
        return jsonify({"error": "Invalid payload format"}), 400
    
    event = request.headers.get("X-GitHub-Event")
    payload = request.get_json()

    if event == "push":
        data = build_push_event(payload=payload)
        if data:
            current_app.events_collection.insert_one(data)
    elif event == "pull_request":
        data = build_pull_request_event(payload=payload)
        if data:
            current_app.events_collection.insert_one(data)
    else:
        return jsonify({"status": "ignored"})
        
    return jsonify({"status": "ok"}), 200
