from flask import Flask
from app.webhook.routes import webhook
from app.api.routes import api_bp
from os import getenv
from app.extensions import init_mongo

# Creating our flask app
def create_app():

    app = Flask(__name__)

    app.logger.setLevel(getenv("LOG_LEVEL", "INFO"))

    app.config.from_mapping(
        MONGO_URI=getenv("MONGO_URI"),
        MONGO_DB_NAME=getenv("MONGO_DB_NAME"),
        MONGO_SERVER_SELECTION_TIMEOUT_MS=int(getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", "5000")),
    )

    init_mongo(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(api_bp)
    
    return app