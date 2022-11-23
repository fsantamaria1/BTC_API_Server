from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
# from server import db
from server.resources import db

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    username = Column(String(20))
    password = Column(String(65))
    manager = Column(Boolean)
    admin = Column(Boolean)
    active = Column(Boolean)

class Timesheet(db.Model): 
    __tablename__ = "timesheet_data"
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    division = Column(String(20))
    job_number = Column(String(10))
    work_order = Column(String(10))
    address = Column(String(45))
    job_date = Column(DateTime())
    arrive_time = Column(DateTime())
    left_time = Column(DateTime())
    notes = Column(String(251))
    signature = Column(String(45))
    complete = Column(Boolean, default=False)
    user_id = Column(String(50))
