from flask import Blueprint, Flask, jsonify
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restx import Api
from marshmallow import ValidationError

from blacklist import BLACKLIST
from ma import ma
from resources.login import Login, login_ns
from resources.logout import Logout, logout_ns

from sql_alchemy import db
from models.token_blocklist import TokenBlocklist

import os

# Heroku database config
DATABASE_URL = os.environ['DB_URL']

app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api')
authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(blueprint, doc='/doc',
          title='Sample Login Python Flask-RestX Application',
          authorizations=authorizations,
          security='api_key'
          )

app.register_blueprint(blueprint)

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'NoneShouldKnowThisSecret'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)

api.add_namespace(login_ns)
api.add_namespace(logout_ns)


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
    return {'message': 'You are not logged in.'}, 401


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


login_ns.add_resource(Login, '/perform')
logout_ns.add_resource(Logout, '/revoke')

if __name__ == '__main__':
    ma.init_app(app)
    app.run(port=5001)
