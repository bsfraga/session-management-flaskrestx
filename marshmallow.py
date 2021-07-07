from flask_marshmallow import Marshmallow

marsh = None

def marshmallow_instance(app):

    marsh = Marshmallow(app)
    return marsh
