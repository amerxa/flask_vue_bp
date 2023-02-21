import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from resources.user import blp as UserBlueprint


def configure_app(app: Flask) -> None:
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JSON_SORT_KEYS"] = False
    app.config["API_TITLE"] = "Flask Vue Boilerplate"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/api"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


def configure_jwt_manager(jwt_manager: JWTManager) -> None:
    @jwt_manager.unauthorized_loader
    def unauthorized_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token.",
                    "error": "authorization_required"}),
            401
        )


def create_app() -> Flask:
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    Migrate(app, db)
    jwt_manager = JWTManager(app)
    configure_jwt_manager(jwt_manager)
    api = Api(app)
    api.register_blueprint(UserBlueprint)
    return app
