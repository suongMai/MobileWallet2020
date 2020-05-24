from flask_restx import fields

response_model = {
    "status": fields.String,
    "error_code": fields.String,
    "error_message": fields.String,
    }

register_model = {
    "email": fields.String,
    "password":fields.String
}
register_response= {
    "token": fields.String,
    "refresh_token":fields.String,
    "error_message":fields.String
}

login_model = {
    "email":fields.String,
    "password":fields.String
}

