'''
Created on May 24, 2020

@author: Suong.Mai
'''

import datetime
import jwt
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity, get_jti, get_raw_jwt)
import datetime
from flask import redirect, jsonify
from flask import current_app as app
import textwrap
from flask_restx import fields, Resource, Namespace, reqparse


from mobilewallet.wallet.models.balanceModel import *
from mobilewallet.common.commonModel import *
from mobilewallet.wallet.services.balanceService import *
from mobilewallet.auth.services.authServices import *

SUCCESS = 'SUCCESS'
PENDDING = 'PENDDING'
ERROR = 'ERROR'




httpResponseBase_response = api.model('HttpResponseModel', httpResponseBase)

 
 
@api.route('/retrieve', doc={"Description": "Retrieve Balance"})
class BalanceRetrieve(Resource):
 
    balance_model = api.model('Balance Response', balance_retrieve_response_model)
    balance_wrapper = {"data": fields.List(fields.Nested(balance_model))}
    http_balance_response = api.inherit(
        'HTTP Balance Response', httpResponseBase_response, balance_wrapper)
 
    @jwt_required
    @api.marshal_with(http_balance_response)
    def get(self):
        uuid = get_jwt_identity()['uuid']
        return HttpResponse(data=retrieveBalance(uuid)), 200
 
 
  
@api.route('/transfer',
     doc={"Description": "Do money transfer from user A(current logged in)  to user B"})
class BalanceTranfer(Resource):
  
    money_transfer_model = api.model("Money Transfer", money_tranfer)
    transfer_response = api.model("Transfer Response", money_tranfer_response)
  
    tranfer_wrapper = {"data":fields.List(fields.Nested(transfer_response))}
    transfer_response_http = api.inherit("mth", httpResponseBase_response, tranfer_wrapper)
  
    @api.expect(money_transfer_model  , validate=True)
    @jwt_required
    @api.marshal_with(transfer_response_http)
    def post(self):
        uuid = get_jwt_identity()['uuid']
        payee = getUserInfo(api.payload.get('payee_email'))
        if payee:
            transaction_record = {}
            transaction_record['payer'] = uuid
            transaction_record['payee'] = payee.get('uuid')
            transaction_record['amount'] = float(api.payload.get('amount'))
            transaction_record['trasaction_date'] = datetime.datetime.now()
            transaction_record['trasaction_message'] = api.payload.get('pament_message')
            payer_wallet_info = retrieveBalance(uuid)
            payee_wallet_info = retrieveBalance(payee.get('uuid'))
              
            payer_tmp_ammount = payer_wallet_info.get('available_ammount') - float(api.payload.get('amount'))
            payee_tmp_ammount = payee_wallet_info.get('available_ammount') + float(api.payload.get('amount'))
              
            if payer_tmp_ammount < 0:
                transaction_record['status'] = ERROR
                transaction_record['description'] = "Balance is low"
                createTransaction(transaction_record)
                return HttpResponse(data={"error_message": "Your balance is low. Can not do this transaction"}, 
                                success=False, message="Tranfer error"), 200
                                  
            elif payee_tmp_ammount > payee_wallet_info.get('wallet_limit', 10000):
                transaction_record['status'] = ERROR
                transaction_record['description'] = "Payee's wallet limit exceeded"
                createTransaction(transaction_record)
                return HttpResponse(data={"error_message": "Payee's wallet limit exceeded"}, 
                                    success=False, message="Tranfer error"), 200
              
            elif float(api.payload.get('amount')) < 0:
                transaction_record['status'] = ERROR
                transaction_record['description'] = "Invalid transfer ammount"
                createTransaction(transaction_record)
                return HttpResponse(data={ "error_message": "Invalid transfer ammount"}, 
                                    success=False, message="Tranfer error"), 200
            else:
                transaction_record['status'] = SUCCESS
                transaction_record['description'] = "success"
                  
                insert = createTransaction(transaction_record)
                if insert:
                    udpateWallet(uuid, payer_tmp_ammount)
                    udpateWallet(payee.get('uuid'), payee_tmp_ammount)
                return HttpResponse(data=transaction_record), 200
        else:
            return HttpResponse(data="",success=False,message="Peyee not found"), 200
   
   
@api.route('/transactions',doc={"Description":"Retrieve transaction list"})
class TracsactionRetrieve(Resource):
    
    transaction_wrapper = {"data":fields.List(fields.Nested(trans_list))}
    transaction_response_http = api.inherit("Money Transfer HTTP",httpResponseBase,transaction_wrapper)
    @jwt_required
    @api.marshal_with(httpResponseBase_response)
    def get(self):
        uuid  = get_jwt_identity()['uuid']
        trans = getUserTracsactionList(uuid)
        return HttpResponse(data={[{"trans":trans.get('data'),
                                   "total_transfer_in_success":trans.get('total_transfer_in_success'),
                                   "total_transfer_out_success":trans.get('total_transfer_out_success')}]}), 200