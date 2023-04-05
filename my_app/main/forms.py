from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, DataRequired, Email, NumberRange

class CreateEnigmaForm( FlaskForm ):
    enigma = StringField(label='Enigma', validators=[InputRequired(), Length(min=1, max=250, message="Une énigme doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    response = StringField(label='Response', validators=[InputRequired(), Length(min=1, max=100, message="La réponse doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    level = IntegerField(label='Level', validators=[InputRequired(), NumberRange(min=0, max=5, message="Le niveau de difficulté doit être compris entre 0 et 5 !")])
    #level = IntegerField(label='Level', validators=[InputRequired(), NumberRange(min=0, max=5)])
    submit = SubmitField('Create')

