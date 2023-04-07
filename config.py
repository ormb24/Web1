import os, binascii
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'vc-dev.db')
    TEMPLATE_AUTO_RELOAD = True
    ENIGMAS_PER_PAGE = 5 #nombre d'énigmes par page, si la pagination est utilisée.

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'vc-prod.db')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}