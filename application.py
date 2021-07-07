from flask import Flask, jsonify, request
from flask_restful import Api
from flask_marshmallow import Marshmallow
import jwt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, app.db) #gotta create a environment variable for this latter
app.config['SECRET_KEY'] = "YouWillNeverKnowThisKey" #gotta create a environment variable for this later

@app.before_first_request
def build_database():
    db.create_all()


api = Api(app)

#--------------------------Endpoints--------------------------#
api.add_resource(resource, key)



if __name__ == '__main__':
    from sql_alchemy import db
    from marshmallow import marshmallow_instance

    db.init_app(app)
    marsh = marshmallow_instance(app)
    app.run(debug=True)