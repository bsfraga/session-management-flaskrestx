from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource, fields
from models.user import UserModel
from werkzeug.security import check_password_hash

login_ns = Namespace('session', description='Perform Login')

login = login_ns.model('login', {
    'username': fields.String('Registered username'),
    'password': fields.String('Password from the respective informed registered username')
})


class Login(Resource):

    @login_ns.expect(login)
    def post(self):
        data = request.get_json()

        if not data or not data['username'] or not data['password']:
            return {"error": "not authenticated"}, 401

        user = UserModel.find_by_username(data['username'])

        if not user:
            return {'message': 'User not found'}, 404

        if check_password_hash(user.password, data['password']):
            token = create_access_token(identity=user.id)
            if token:
                user.track_last_login_datetime()
            return {'token': token,
                    'message': "User successfully logged in."}, 200

        # return {'error': "bad request"}, 401
