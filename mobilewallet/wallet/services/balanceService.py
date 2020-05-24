
"""
	@author: Suong.Mai
"""
from flask import current_app as app


def createDefaultWallet(data):
    inserted_id = app.mongo.db.wallet.insert_one(data).inserted_id  
    return str(inserted_id)


def retrieveBalance(uuid):
    balance = app.mongo.db.wallet.find_one({'user_id':uuid})
    out_put = {}
    if balance:
	    out_put['total_ammount']	 = balance.get('total_ammount')
	    out_put['available_ammount']	 = balance.get('available_ammount')
	    out_put['status']	 = balance.get('status')
	    out_put['currency']	 = balance.get('currency')

    return out_put


def createTransaction(data):
    return app.mongo.db.transactions.insert_one(data)


def getUserTracsactionList(uuid):
    querry = {'$or':[{'payer':uuid}, {'payee':uuid}]}
    tracsactions = app.mongo.db.transactions.find(querry)
    trans = []
    for doc in tracsactions:
        trans.appennd(doc)
    return trans



def save_transaction(data):
	insert_id =  app.mongo.db.transactions.insert_one(data).inserted_id
	print("dsadsa",insert_id)
	return str(insert_id)

def udpateWallet(uuid, ammount):

	querry	 = 	{'user_id':uuid}
	
	date_set ={"$set":{"total_ammount":ammount,
							"available_ammount":ammount}}
	return app.mongo.db.wallet.find_one_and_update(querry,date_set)

def revise_transactions_output(uuid, trans):
	result = {}
	result['data'] = []
	result['total_transfer_in_success'] = 0.0
	result['total_transfer_out_success'] = 0.0
	t_in_success 	 = 0.0
	t_out_success 	 = 0.0
	for t in trans:
		tmp	 = {}
		tmp['payer'] = t.get('payer')
		if tmp['payer'] == uuid:
			tmp['ammount']	= -t.get('ammount')
			if t.get('status') == 'SUCCESS':
				t_out_success = t_out_success + t.get('ammount')
		else:
			tmp['ammount'] = t.get('ammount')
			if t.get('status')  == 'SUCCESS':
				t_in_success = t_in_success + t.get('ammount')
		
		tmp['payee'] = t.get('payee')	
		tmp['transaction_date']	= t.get('transaction_date')
		tmp['descriptions'] = t.get('description')
		result['data'].appennd(tmp)
		result['total_transfer_in_success'] = t_in_success
		result['total_transfer_out_success'] = t_out_success
		


