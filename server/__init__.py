from flask import Flask
from server.resources import db

def create_app(configuration_mode):
    app = Flask( __name__, instance_relative_config=False)
    #configure and initalize app
    app.config.from_object(configuration_mode)
    db.init_app(app)
    with app.app_context():
        # Server routes
        from server.routes import users
        from server.routes import login
        # Create db if it doesn't exist
        db.create_all()
        return app