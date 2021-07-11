from flask_restx.fields import DateTime
from sql_alchemy import db
from typing import List
import datetime

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime)
    last_email_change = db.Column(db.DateTime)
    last_pswd_change = db.Column(db.DateTime)
 
    def __init__(self, name, username, email, password, level):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.level = level


    def __repr__(self):
        return f'UserModel(name={self.name}, username={self.username}, email={self.email})'

    def json(self):
        return {'name': self.name, 'username': self.username, 'email': self.email}

    @classmethod
    def find_by_name(cls, name) -> 'UserModel':
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_username(cls, username) -> 'UserModel':
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id) -> 'UserModel':
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def track_last_login_datetime(self) -> None:
        self.last_login = datetime.datetime.now()
        db.session.commit()

    def track_last_email_change(self) -> None:
        self.last_email_change = datetime.datetime.now()
        db.session.commit()

    def track_last_pswd_change(self) -> None:
        self.last_pswd_change = datetime.datetime.now()
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
