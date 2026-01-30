from flask import Blueprint, current_app, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/events", methods=["GET"])
def get_events():
    since = request.args.get("since")

    query = {}
    if since:
        query["timestamp"] = {"$gt": since}

    events = list(
        current_app.events_collection
        .find(query, {"_id": 0})
        .sort("timestamp", 1)
        .limit(20)
    )

    return jsonify(events), 200
