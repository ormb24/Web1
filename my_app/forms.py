from my_app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

class PasswordForm( FlaskForm ):
    password = PasswordField(label='Password', validators=[InputRequired(),Length(min=8, message="Password shoud be at least %(min)d characters long")])
    submit = SubmitField('Send')

class CreateEnigmaForm( FlaskForm ):
    enigma = StringField(label='Enigme', validators=[InputRequired(), Length(min=20, max=250, message="Une énigme doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    response = StringField(label='Reponse', validators=[InputRequired(), Length(min=1, max=100, message="La réponse doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    level = IntegerField(label='Niveau', validators=[InputRequired(), Length(min=1, max=5, message="Le niveau de difficulté doit être compris entre 1 et 5 !")])

class LoginForm( FlaskForm):
    username = StringField(label='Username:', validators=[InputRequired(), Length(min=2, max=20, message="Le nom de l\'utilisateur doit posséder entre %(min)d et %(max)d caractères'")])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8, message="Le mot de passe doit comprendre au moins %(min)d caractères !")])
    submit = SubmitField('Envoyer')
