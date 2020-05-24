import os

#todo: push all creaentials to enviroment variable
if os.environ.get('ENV') is not None:
    MONGO_URI = "mongodb+srv://{}:{}@{}:27017/{}".format(os.environ.get('MONGO_USER'),os.environ.get('MONGO_PASS'),os.environ.get('MONGODB_HOSTNAME'),os.environ.get('MONGO_DB'))
else:
    MONGO_URI = "mongodb+srv://wallet2020:wallet2020@cluster0-h78d3.gcp.mongodb.net/wallet2020?retryWrites=true&w=majority"\

JWT_SECRET_KEY = "this-is-secrect"



