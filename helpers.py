from flask import jsonify, json, request
from functools import wraps
from models import User
import secrets
import decimal

def token_required(your_function):
    @wraps(your_function)
    def decoration(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"].split(" ")[1]
        if not token:
            return jsonify({"ERROR": "Sorry, token is missing"})
        
        try:
            user_token = User.query.filter_by(token = token).first()
            
        except:
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({"ERROR": "Sorry, wrong token"})
            
        return your_function(user_token, *args, **kwargs)
    return decoration

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)