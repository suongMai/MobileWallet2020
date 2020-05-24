"""
    @author: Suong.Mai
"""


import datetime
import jwt
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity, get_jti, get_raw_jwt)
from mobilewallet.auth.models.authModel import *
from mobilewallet.auth.services.authServices import *
from mobilewallet.common.commonModel import *
from mobilewallet.wallet.services.balanceService import *
import datetime
from flask import redirect,jsonify
from flask import current_app as app
import textwrap
from flask_restx import fields,Resource, Namespace,reqparse
import uuid


api = Namespace('auth',description="Auth controller")

httpResponseBase_response = api.model('HttpResponseModel',httpResponseBase)


# flask_bcrypt =  Bcrypt(app)

@api.route('/register',doc={"Description":"Get reference code"})
class AuthRegister(Resource):
    register = api.model('Register Model',register_model)
    response_model = api.model("RegisterResponse",register_response)
    
    register_wrapper = {"data":fields.List(fields.Nested(response_model))}
    register_respone_model = api.inherit('HTTP Register Response Model',httpResponseBase_response,register_wrapper)

    @api.expect(register,validate=True)
    @api.marshal_with(register_respone_model)
    def post(self):
        if_user_present =  getUserInfo(api.payload.get('email'))
        if if_user_present:
            return HttpResponse(data={"error_message":"This user already exists"},success=False), 409
        else:
            """hash the password""" 
            api.payload['uuid']         = str(uuid.uuid4())
            api.payload['password']     = app.flask_bcrypt.generate_password_hash(api.payload['password'], 10).decode('utf-8')
            api.payload['createDate']   = datetime.datetime.now()
            generate_identity = {
                "email":api.payload['email'],
                "uuid":api.payload['uuid']
            }
            createUser(api.payload)
            response = {}
            default_wallet = {}

            response['token']           =   create_access_token(identity=generate_identity, fresh=True)
            response['refresh_tokne']   =   create_refresh_token(identity=generate_identity)

            """create a defaukt walet with 20 SGD"""
            default_wallet['total_ammount']     = 20.0
            default_wallet['available_ammount'] = 20.0
            default_wallet['wallet_limit']      = 10000
            default_wallet['currency']         = 'SGD'
            default_wallet['status']            = 'ACTIVE'
            default_wallet['user_id']           = api.payload['uuid']
            default_wallet['createDate']           = datetime.datetime.now()
            default_wallet['updateDate']           = datetime.datetime.now()
            createDefaultWallet(default_wallet)

            return HttpResponse(data=response), 200

@api.route('/login',doc={"Description":"Get reference code"})
class AuthLogin(Resource):
    
    login = api.model('Register Model',login_model)
    response_model = api.model("Login Response",register_response)
    
    login_wrapper = {"data":fields.List(fields.Nested(response_model))}
    login_respone_model = api.inherit('HTTP Login Model',httpResponseBase_response,login_wrapper)

    @api.expect(login,validate=True)
    @api.marshal_with(login_respone_model)
    def post(self):

        user =  getUserInfo(api.payload.get('email'))
        if user:
            password = user.get('password')
            if app.flask_bcrypt.check_password_hash(password,api.payload['password']):
                response = {}
                generate_identity = {
                    "email":user.get('email'),
                    "uuid":user.get('uuid')
                }
                response['token']           =   create_access_token(identity=generate_identity, fresh=True)
                response['refresh_tokne']   =   create_refresh_token(identity=generate_identity)
                return HttpResponse(data=response), 200
            else:
                return HttpResponse(data={"error_message":"Invalid password"},success=False), 401
        else:
            return HttpResponse(data={"error_message":"Invalid user"},success=False), 404
            
