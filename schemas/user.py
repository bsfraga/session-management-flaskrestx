from sqlalchemy.orm import load_only
from models.user import UserModel
from ma import ma
from marshmallow_sqlalchemy import auto_field

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("id", "password",)