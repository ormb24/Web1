from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms.validators import Length, DataRequired, NumberRange

from unidecode import unidecode
from my_app.models import Riddle


# Vérifie la liste des mots autorisés pour l'énigme.
def validate_riddle(form,field):
    not_accepted_words = ['enigme','reponse'] #liste non exhaustive...
    strField = (unidecode(field.data)).lower()  #retire les accents et met en minuscules
    for word in not_accepted_words:
        if word in strField:
            form.riddle.errors.append("Le mot \'{}\' n'est pas autorisé !".format(field.data))

# Vérifie si la valeur du champ n'est pas déjà présente en DB
#def isUnique_riddle(form, field):
#    if Riddle.query.filter_by(riddle=field.data).first():
#        form.riddle.errors.append("L'énigme existe déjà en DB !")

class RiddleForm( FlaskForm ):
    id = HiddenField("riddle_id")
    riddle = StringField("Enigme : ",
                           validators=[DataRequired(message="Le champ ne peut être vide !"),
                                       Length(min=10,max=250, message="L\'énigme doit comporter entre %(min)d et %(max)d caractères !"),
                                       validate_riddle])
    answer = StringField("Réponse : ",
                           validators=[DataRequired(message="Le champ ne peut être vide !"),
                                       Length(max=100, message="La réponse ne peut comporter plus de %(max)d caractères !"),
                                       validate_riddle])
    clue = StringField("Indice : ",
                       validators=[Length(max=100, message="L'indice ne peut comporter plus de %(max)d caractères !")])
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