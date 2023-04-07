from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, DataRequired, Email, NumberRange

class CreateEnigmaForm( FlaskForm ):
    enigma = TextAreaField(label='Enigme : ',render_kw={"rows":3,"cols":80},validators=[InputRequired(), Length(min=1, max=250,message="Une énigme doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    #enigma = StringField(label='Enigme : ', validators=[InputRequired(), Length(min=1, max=250, message="Une énigme doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    response = StringField(label='Reponse : ',render_kw={"size":77}, validators=[InputRequired(), Length(min=1, max=100, message="La réponse doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    level = IntegerField(label='Niveau : ', validators=[InputRequired(), NumberRange(min=0, max=10, message="Le niveau de difficulté doit être compris entre 0 et 5 !")])
    submit = SubmitField('Ajouter')

