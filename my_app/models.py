from my_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from my_app import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    blocked = db.Column(db.Boolean, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, password, firstname, lastname):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.blocked = False
        self.admin = False
    def __repr__(self):
        rep = "User : {}, {}\nEmail : {}".format(self.lastname, self.firstname, self.email)
        return rep
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id



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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    riddle = db.Column(db.String(250), unique=True, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref=db.backref('riddle'))
    user = db.relationship('User', backref=db.backref('riddles', lazy=True))

    def __init__(self, riddle, answer, level, user_id):
        self.riddle = riddle
        self.answer = answer
        self.level = level
        self.user_id = user_id
    def __repr__(self):
        repr = "id : {}, riddle : {}, answer : {}, level : {}, uid : {}".format(self.id, self.riddle, self.answer, self.level, self.user_id)
        return repr
    def set_level(self,level):
        self.level = level