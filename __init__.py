from flask import Flask
from resources.models import db

def create_app():
    app = Flask( __name__)
    #configure app
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\fsantamaria\\OneDrive - Berry-It\\Documents\\VS Code Files\\timesheets2.db'
    # Create db if it doesn't exist
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app