import uuid
import jwt
from functools import wraps

from flask import jsonify, request
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from sql_alchemy import db
from model.user import UserModel

def token_required(f):
    @wraps(f)
    def decorated(*arg, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message' : 'Token is missing.'}, 401
        
        try:
            data = jwt.decode(token, key='ThisShouldKeepAsASecret')
            current_user = UserModel.query.filter_by(public_id=data['public_id']).first()
        except:
            return {'message': 'Token is invalid'}, 401
    
    return decorated

class NewUser(Resource):

    def post(self):
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = UserModel()