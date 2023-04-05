from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, DataRequired, Email
class LoginForm( FlaskForm ):
    #username = StringField(label='Username:', validators=[InputRequired(), Length(min=2, max=20, message="Le nom de l\'utilisateur doit posséder entre %(min)d et %(max)d caractères'")])
    email = StringField('Email', validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, message="Le mot de passe doit comprendre au moins %(min)d caractères !")])
    submit = SubmitField('Log in')

#class PasswordForm( FlaskForm ):
#    password = PasswordField(label='Password', validators=[InputRequired(),Length(min=8, message="Password shoud be at least %(min)d characters long")])
#    submit = SubmitField('Send')