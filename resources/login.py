from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from models.user import UserModel
from werkzeug.security import check_password_hash

login_ns = Namespace('login', description='Perform Login')

login = login_ns.model('login', {
    'username': fields.String('Registered username'),
    'password': fields.String('Password from the respective informed registered username')
})

class Login(Resource):

    @login_ns.expect(login)
    def post(self):
        auth = request.get_json()

        print(auth)

        if not auth or not auth['username'] or not auth['password']:
            return {"error": "not authenticated"}, 401

        user = UserModel.query.filter_by(username=auth['username']).first()

        if not user:
            return {'message': 'User not found'}, 404

        if not user:
            return {"error": "user not found"}, 404

        if check_password_hash(user.password, auth['password']):
            token = create_access_token(identity=user.id)
            return {'token': token,
                    'message': "User successfully logged in."}, 200

        return {'error':"bad request"}, 401
