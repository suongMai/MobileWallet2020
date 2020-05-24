
"""
	@author: Suong.Mai
"""
from flask_restx import fields, Resource, Namespace, reqparse

api = Namespace('balance', description="Balance controller")

from flask_restx import fields

balance_retrieve_response_model = {
	"total_ammount":fields.Float,
	"available_ammount":fields.Float,
	"status":fields.String,
	"currency":fields.String
}

money_tranfer = {
	"payee_email":fields.String,
	"amount":fields.Float,
	"pament_message":fields.String,
	
}
money_tranfer_response = {
	"payer":fields.String,
	"amount":fields.Float,
	"trasaction_message":fields.String,
	"error_message":fields.String
}	

money_tranfer_response_model = {
	"status":fields.Boolean,
	"message":fields.String,
}


transaction_detail_model = api.model('Trans model',{
	"payer":fields.String,
	"payee":fields.String,
	"payment_type":fields.String,
	"status":fields.String,
	"ammount":fields.Float,
	"transaction_date":fields.DateTime(dt_format='rfc822'),
	"payment_message":fields.String,
	"descriptions":fields.String
})


trans_list = api.model('Trans list response',{
		"trans":fields.List(fields.Nested(transaction_detail_model)),
		"total_transfer_out_success":fields.Float,
		"total_transfer_in_success":fields.Float
	})

