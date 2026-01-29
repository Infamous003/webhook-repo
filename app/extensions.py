from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def init_mongo(app):
    mongo_uri = app.config.get("MONGO_URI")
    db_name = app.config.get("MONGO_DB_NAME")
    mongo_timeout_ms = app.config.get("MONGO_SERVER_SELECTION_mongo_", 10000)

    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in the app configuration")

    if not db_name:
        raise ValueError("MONGO_DB_NAME is not set in the app configuration")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=mongo_timeout_ms)
        client.admin.command("ping")

        app.mongo_client = client
        app.mongo_db = client[db_name]
        app.events_collection = app.mongo_db["events"]

        app.logger.info("Successfully connected to MongoDB")
    except ConnectionFailure as e:
        app.logger.error(f"MongoDB connection failed: {e}")
        raise
