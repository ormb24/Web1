from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, DataRequired, Email, NumberRange

from my_app.models import Riddle


class CreateEnigmaForm( FlaskForm ):
    enigma = TextAreaField(label='Enigme : ',render_kw={"rows":3,"cols":80},validators=[InputRequired(), Length(min=1, max=250,message="Une énigme doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    #enigma = StringField(label='Enigme : ', validators=[InputRequired(), Length(min=1, max=250, message="Une énigme doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    response = StringField(label='Reponse : ',render_kw={"size":77}, validators=[InputRequired(), Length(min=1, max=100, message="La réponse doit comprendre au moins %(min)d caractères; et au plus %(max)d caractères.")])
    level = IntegerField(label='Niveau : ', validators=[InputRequired(), NumberRange(min=0, max=10, message="Le niveau de difficulté doit être compris entre 0 et 5 !")])
    submit = SubmitField('Ajouter')


# Vérifie la liste des mots autorisés pour l'énigme.
def validate_riddle(form,field):
    not_accepted_words = ['énigme','réponse'] #liste non exhaustive...
    strField = field.data #because StringField, TextField,... are not iterable; get their content first !
    for word in not_accepted_words:
        if word in strField:
            form.riddle.errors.append("Le mot \'{}\' n'est pas autorisé !".format(word))

# Vérifie si la valeur du champ n'est pas déjà présente en DB
def isUnique_riddle(form, field):
    if Riddle.query.filter_by(riddle=field.data).first():
        form.riddle.errors.append("L'énigme existe déjà en DB !")


class RiddleForm( FlaskForm ):
    id = HiddenField("riddle_id")
    riddle = StringField("Enigme : ",
                           validators=[DataRequired(message="Le champ ne peut être vide !"),
                                       Length(max=250, message="L\énigme ne peut comporter plus de %(max)d caractères !"),
                                       validate_riddle,
                                       isUnique_riddle])
    answer = StringField("Réponse : ",
                           validators=[DataRequired(message="Le champ ne peut être vide !"),
                                       Length(max=100, message="La réponse ne peut comporter plus de %(max)d caractères !")])
    level = IntegerField("Niveau : ",
                         validators=[DataRequired(message="Veuillez entrer une valeur !"),
                                     NumberRange(min=0, max=10, message="Le niveau de difficulté doit être compris entre %(min)d et %(max)d !")
                                                        ])
    submit = SubmitField("Ajouter")

class ClueForm( FlaskForm ):
    id = HiddenField("clue_id")
    clue = StringField("Clue : ",
                       validators=[Length(max=100, message="L\'indice ne peut comporter plus de %(max)d caractères !")])
    riddle = StringField("Enigme :", render_kw={'readonly': True})
    riddle_id = HiddenField("riddle_id")
    submit = SubmitField("Ajouter")