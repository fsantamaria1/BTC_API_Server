#Default config class
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'thisissecret'

#Class used to run app in development mode
class Dev(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'

