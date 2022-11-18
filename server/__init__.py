from flask import Flask
from server.resources.models import db

def create_app(configuration_mode):
    app = Flask( __name__)
    #configure app
    app.config.from_object(configuration_mode)
    # Create db if it doesn't exist
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app