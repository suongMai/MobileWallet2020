
from flask import current_app as app

def createUser(data):
    inserted_id = app.mongo.db.users.insert_one(data).inserted_id
    return str(inserted_id)


def getUserInfo(email):
    user = app.mongo.db.users.find_one({"email":email})
    if user and  user.get('uuid'):
        return user
    else:
        return None





