import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
import models

from resources.accounts import blp as AccountBlueprint
from resources.revenues import blp as RevenueBlueprint
from resources.categories import blp as CategoryBlueprint
from resources.recurrents import blp as RecurrentBlueprint
from resources.goals import blp as GoalsBlueprint

# Factory function for starting and configuring flask, for testing purposes
def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True  # extension exceptions will be raised
    app.config["API_TITLE"] = "Budget Tracker API"  # smorest - doc title
    app.config["API_VERSION"] = "v1"  # smorest - doc api version
    app.config["OPENAPI_VERSION"] = "3.0.3"  # smorest to use doc standard 3.0.3
    app.config["OPENAPI_URL_PREFIX"] = "/"  # tells smorest what the route of the api is
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # smorest uses swagger ui
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # If create_app doesn't have a db url, it'll search for local environment variable or default to sqlite
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # soon to be deprecated, slows down sqlalchemy

    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "secret"
    jwt = JWTManager(app)

    # runs everytime server recieves a JWT token
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    # if the JWT token is revoked
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has been revoked", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has expired.", "error": "token_expired"}
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error": "authorization_required"
                }
            ),
            401,
        )
    
    # Creates the database from the imported models module
    with app.app_context():
        db.create_all()

    api.register_blueprint(AccountBlueprint)
    api.register_blueprint(RevenueBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(RecurrentBlueprint)
    api.register_blueprint(GoalsBlueprint)

    return app