from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from models.user import UserModel
from schemas.user import UserSchema
from sql_alchemy import db
from werkzeug.security import generate_password_hash, check_password_hash

newuser_schema = UserSchema()
users_list_schema = UserSchema(many=True)
user_schema = UserSchema()

userdoc_ns = Namespace('user', description='User management')

newuser = userdoc_ns.model('new_user', {
    'name': fields.String('Your name'),
    'username': fields.String('Your desired username'),
    'email': fields.String('Your e-mail address'),
    'password': fields.String('Your password')
})

userdoc = userdoc_ns.model('single_user', {
    'name': fields.String('Your name'),
    'username': fields.String('Your desired username'),
    'email': fields.String('Your e-mail address'),
    'level': fields.String('Your level of permission')
})

user_doc_list = userdoc_ns.model('multiple_users', {
    'users': fields.List(fields.Nested(userdoc))
})

userdoc_del = userdoc_ns.model('delete', {
    'message': fields.String("")
})

userdoc_put = userdoc_ns.model('user_put', {
    'email': fields.String("New e-mail address"),
    'username': fields.String("New username")
})


class User(Resource):

    @userdoc_ns.expect(newuser)
    def post(self):
        data = request.get_json()

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        data['level'] = 3
        data['password'] = hashed_password
        new_user = newuser_schema.load(data)

        db.session.add(new_user)
        db.session.commit()

        return newuser_schema.dump(new_user), 201

    @jwt_required(locations=["headers"])
    @userdoc_ns.response(200, description='', model=userdoc)
    def get(self, name):
        user = UserModel.find_by_name(name)

        if not user:
            return {"message": "User not found."}, 404

        return user_schema.dump(user), 200

    @jwt_required(locations=["headers"])
    def delete(self, id):
        own_id = get_jwt_identity()

        user = UserModel.find_by_id(own_id)

        if not user:
            return {"message": "User not found."}, 404

        if user.level < 1:
            return {"message": "Your're not allowed to perform this action"}, 401

        user_to_del = UserModel.find_by_id(id)
        user_to_del.delete_from_db()

        return {"message": f"User id[{id}] has bem deleted."}, 200

    @jwt_required(locations=["headers"])
    @userdoc_ns.expect(userdoc_put)
    def put(self, id):
        user = UserModel.find_by_id(id)
        data = request.get_json()

        if user:
            if user.email and data['email'] != user.email:
                user.track_last_email_change()
            if user.password and data['password'] != check_password_hash(user.password, data['password']):
                user.track_last_pswd_change()

            user.email = data['email'] if data['email'] else user.email
            user.password = generate_password_hash(data['password'], method='sha256') if data['password'] else user.password
        else:
            data = user_schema.load(user)

        user.save_to_db()
        return user_schema.dump(user), 200

class Users(Resource):

    @jwt_required(locations=["headers"])
    @userdoc_ns.header("Authorization")
    @userdoc_ns.response(200, description="Get all users", model=user_doc_list)
    def get(self):
        return users_list_schema.dump(UserModel.find_all()), 200
