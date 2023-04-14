from my_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from my_app import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "username = %s, email = %s" % (self.username, self.email)

class Enigma(db.Model):
    __tablename__ = 'enigmas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enigma = db.Column(db.String(250), unique=True, nullable=False)
    response = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, enigma, response, level):
        self.enigma = enigma
        self.response = response
        self.level = level
    def set_level(self,level):
        self.level = level

    def __repr__(self):
        return "Enigma = %s; Solution = %s; Level = %i" % (self.enigma,self.response, self.level)


class Riddle(db.Model):
    __tablename__ = 'riddles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    riddle = db.Column(db.String(250), unique=True, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        rep = "id : {}, riddle : {}, answer : {}, level : {}".format(self.id, self.riddle, self.answer, self.level)
        return rep

