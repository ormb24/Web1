from my_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from my_app import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Riddle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    riddle = db.Column(db.String(250), unique=True, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    clues = db.relationship('Clue', backref='riddle', cascade="delete, delete-orphan")

    def getid(self):
        return self.id
    #def __init__(self, riddle, answer, level, user_id,user=None):
    #    self.riddle = riddle
    #    self.answer = answer
    #    self.level = level
    #    self.user_id = user_id

    def __repr__(self):
        repr = "id : {}, riddle : {}, answer : {}, level : {}".format(self.id, self.riddle, self.answer, self.level)
        return repr
    def set_level(self,level):
        self.level = level

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    blocked = db.Column(db.Boolean, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    riddles = db.relationship('Riddle', backref='user')

    def __init__(self, email, password, firstname, lastname, username):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.blocked = False
        self.admin = False
    def __repr__(self):
        rep = "User : {}, {}\nEmail : {}".format(self.lastname, self.firstname, self.email)
        return rep
    def set_password(self, password):
        #self.password_hash = generate_password_hash(password)
        self.password = generate_password_hash(password)

    def check_password(self, password):
        #return check_password_hash(self.password_hash, password)
        return check_password_hash(self.password, password)
    def get_username(self):
        return self.username
    def get_id(self):
        return self.id


class Clue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clue = db.Column(db.String(100))
    riddle_id = db.Column(db.Integer, db.ForeignKey('riddle.id'), nullable=False)

    def __repr__(self):
        repr = "id : {}, clue : {}, riddle_id : {}".format(self.id,self.clue,self.riddle_id)
        return repr