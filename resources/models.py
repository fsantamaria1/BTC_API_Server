from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(65))
    manager = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

class Timesheet(db.Model): 
    __tablename__ = "timesheet_data"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    division = db.Column(db.String(20))
    job_number = db.Column(db.String(10))
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)