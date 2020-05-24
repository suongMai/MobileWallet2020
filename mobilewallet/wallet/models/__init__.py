from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api
from flask import Blueprint
from flask_jwt_extended import (JWTManager)
from flask_cors import CORS


def create_app(config_object='invitation.config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    with app.app_context():
        app.mongo = PyMongo()
        app.mongo.init_app(app)
        app.jwt = JWTManager(app)
    CORS(app,support_credentials=True)
    from invitation.controllers.invitationController  import api as invitation
    api = Api(app, title="invitaion Service API Documentation", description="",)
    api.add_namespace(invitation)
    return app