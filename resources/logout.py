import datetime
from models.token_blocklist import TokenBlocklist
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from models.user import UserModel
from werkzeug.security import check_password_hash
from sql_alchemy import db


logout_ns = Namespace('logout', description='Perform Login')

logout = logout_ns.model('Logout', {
    'username': fields.String('Registered username'),
    'password': fields.String('Password from the respective informed registered username')
})

class Logout(Resource):

    @jwt_required(locations=["headers"])
    def delete(self):
        jti = get_jwt()["jti"]
        now = datetime.datetime.now(datetime.timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return {'message':"Token revoked."}
