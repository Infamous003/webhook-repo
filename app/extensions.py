from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

mongo_client = None

def init_mongo(app):
    global mongo_client
    mongo_uri = app.config.get("MONGO_URI")
    server_selection_timeout_ms = app.config.get("MONGO_SERVER_SELECTION_TIMEOUT_MS", 10000)

    if not mongo_uri:
        app.logger.error("MONGO_URI is not set in the app configuration.")
        raise ValueError("MONGO_URI is not set in the app configuration.")

    try:
        mongo_client = MongoClient(
            mongo_uri, 
            serverSelectionTimeoutMS=server_selection_timeout_ms,
        )
        mongo_client.admin.command("ping")
        app.logger.info("Successfully connected to MongoDB.")
    except ConnectionFailure as e:
        app.logger.error(f"Couldn't connect to MongoDB: {e}")
        raise ConnectionError("Failed to connect to MongoDB with the provided MONGO_URI.")