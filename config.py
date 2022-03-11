import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mytodo:study#CCC3@localhost:3306/mytodo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "temperory_Secret_key"