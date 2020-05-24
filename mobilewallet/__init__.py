from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api
from flask import Blueprint
from flask_jwt_extended import (JWTManager)
from flask_cors import CORS
from flask_bcrypt import Bcrypt

def create_app(config_object='mobilewallet.config'):
    app = Flask(__name__)
    app.flask_bcrypt = Bcrypt(app)

    app.config.from_object(config_object)
    with app.app_context():
        app.mongo = PyMongo()
        app.mongo.init_app(app)
        app.jwt = JWTManager(app)

    CORS(app,support_credentials=True)
    from mobilewallet.auth.controllers.authController  import api as auth
    from mobilewallet.wallet.controllers.balanceController import api as balance
    api = Api(app, title="MobileWallet2020 Service API Documentation", description="",)
    api.add_namespace(auth)   
    api.add_namespace(balance)
    return app