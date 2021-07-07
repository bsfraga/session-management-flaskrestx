from flask import request, jsonify, make_response
from flask_restful import Resource
from werkzeug.security import check_password_hash

import jwt
import datetime

from model.user import user_model as user

class Login(Resource):
    
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return {"error" : "not authenticated"}, 401

        user = User.query.filter_by(username=auth.username).first()

        if not user:
            return {"error" : "user not found"}, 404

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id,
                                'expirationTime': datetime.datetime.utcnow()+datetime.timedelta(60),
                                'key': 'ThisShouldKeepAsASecret'})
            return jsonify(token=token.decode('UTF-8'), 
                            message="User successfully logged in."), 200

        return jsonify(error="bad request"), 401