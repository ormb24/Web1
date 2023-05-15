import os, binascii
# Returns a normalized absolutized version of the pathname passed as argument.
# Note : so the path is given correctly, whatever the underlying OS used.
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # Used for generating cryptographic signatures by Flask-WTF to protect forms against CSRF
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    # False : uses less memory, unless signals for object changes are neeeded.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/vc-dev.db')
    TEMPLATE_AUTO_RELOAD = True
    ENIGMAS_PER_PAGE = 5 #nombre d'énigmes par page, si la pagination est utilisée.
    LEVEL_MIN = 0   #Niveau minimum pour une énigme
    LEVEL_MAX = 10  #Niveau maximum pour une énigme

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/vc-prod.db')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}