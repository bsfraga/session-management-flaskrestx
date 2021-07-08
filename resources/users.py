from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from models.user import UserModel
from schemas.user import UserSchema
from werkzeug.security import check_password_hash, generate_password_hash
from sql_alchemy import db
from flask import request
newuser_schema = UserSchema()

newuser_ns = Namespace('user', description='User management')

newuser = newuser_ns.model('new_user', {
    'name': fields.String('Your name'),
    'username': fields.String('Your desired username'),
    'email': fields.String('Your e-mail address'),
    'password': fields.String('Your password')
})


class NewUser(Resource):

    @newuser_ns.expect(newuser)
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


users_list_schema = UserSchema(many=True)
user_schema = UserSchema()

userdoc_ns = Namespace('user', description='User management')

userdoc = userdoc_ns.model('single_user', {
    'name': fields.String('Your name'),
    'username': fields.String('Your desired username'),
    'email': fields.String('Your e-mail address'),
    'level': fields.String('Your level of permission')
})

user_doc_list = userdoc_ns.model('multiple_users', {
    'users': fields.List(fields.Nested(userdoc))
})


class GetUsers(Resource):

    @jwt_required(locations=["headers"])
    @userdoc_ns.header("Authorization")
    @userdoc_ns.response(200, description="Get all users", model=user_doc_list)
    def get(self):
        return users_list_schema.dump(UserModel.find_all()), 200


class GetUserByName(Resource):

    @jwt_required(locations=["headers"])
    @userdoc_ns.response(200, description='', model=userdoc)
    def get(self, name):

        user = UserModel.find_by_name(name)

        if not user:
            return {"message": "User not found."}, 404

        return user_schema.dump(user), 200


userdoc_del = userdoc_ns.model('delete', {
    'message': fields.String("")
})


class DeleteUserById(Resource):

    @jwt_required(locations=["headers"])
    def delete(self, id):
        own_id = get_jwt_identity()

        user = UserModel.find_by_id(id)

        if not user:
            return {"message": "User not found."}, 404

        if user.level < 1:
            return {"message": "Your're not allowed to perform this action"}, 401

        user.delete_from_db()

        return {"message": f"User id[{id}] has bem deleted."}, 200


userdoc_put = userdoc_ns.model('user_put', {
    'email': fields.String("New e-mail address"),
    'username': fields.String("New username")
})


class UpdateUserById(Resource):

    @jwt_required(locations=["headers"])
    @userdoc_ns.expect(userdoc_put)
    def put(self, id):
        user = UserModel.find_by_id(id)
        data = request.get_json()

        if user:
            user.email = data['email']
            user.username = data['username']
        else:
            data = user_schema.load(user)

        user.save_to_db()
        return user_schema.dump(user), 200
