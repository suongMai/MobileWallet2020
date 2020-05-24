"""
    @author: Suong.Mai
"""


from flask_restx import fields


class HttpResponse:
    data = {}
    success = ""
    message = ""
    error_code = ""

    def __init__(self, message="", error_code="", data={}, success=True):
        self.data = data
        self.message = message
        self.error_code = error_code
        self.success = success


httpResponseBase = {
    "error_code": fields.String,
    "message": fields.String,
    "success": fields.Boolean
}