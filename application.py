from flask import Blueprint, Flask, jsonify
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restx import Api
from marshmallow import ValidationError

from blacklist import BLACKLIST
from ma import ma
from resources.login import Login, login_ns
from resources.logout import Logout
from resources.users import NewUser, UpdateUserById, GetUsers, GetUserByName, DeleteUserById, userdoc_ns, newuser_ns

from sql_alchemy import db
from models.token_blocklist import TokenBlocklist

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
authorizations = {
    'api_key' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization'
    }
}
api = Api(blueprint, doc='/doc',
          title='Sample Login Python Flask-RestX Application',
          authorizations=authorizations)
app.register_blueprint(blueprint)

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'NoneShouldKnowThisSecret'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(login_ns)
api.add_namespace(newuser_ns)
api.add_namespace(userdoc_ns)

@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

@jwt.revoked_token_loader
def invalid_token(jwt_header, jwt_payload):
    return {'message': 'Your are not logged in.'}, 401


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


login_ns.add_resource(Login, '/perform')
login_ns.add_resource(Logout, '/revoke')
newuser_ns.add_resource(NewUser, '/new')
userdoc_ns.add_resource(GetUsers, '/all')
userdoc_ns.add_resource(GetUserByName, '/<string:name>')
userdoc_ns.add_resource(DeleteUserById, '/<int:id>')
userdoc_ns.add_resource(UpdateUserById, '/<int:id>')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
