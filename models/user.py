from sql_alchemy import db
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

    @classmethod
    def find_by_username(cls, username) -> 'UserModel':
        return cls.query.filter_by(username=username).first()

    def track_last_login_datetime(self) -> None:
        self.last_login = datetime.datetime.now()
        db.session.commit()
