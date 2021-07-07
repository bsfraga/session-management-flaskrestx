from model.user import UserModel
from marshmallow import marsh

class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_fk = True