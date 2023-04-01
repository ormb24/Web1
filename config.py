import os, binascii
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'vc.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
