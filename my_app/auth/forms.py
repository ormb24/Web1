from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, DataRequired, Email

from my_app.models import User

def isUnique_email(form, field):
    if User.query.filter_by(email=field.data).first():
        form.email.errors.append("Email address : \'{}\' is already registered ! Choose another one...".format(field.data))

class RegisterForm( FlaskForm ):
     email = StringField('Email : ', validators=[Email(message="Please fill in a valid email address !"),
                                              InputRequired(),
                                              Length(min=5,max=120),
                                              isUnique_email])
     password = PasswordField('Password : ', validators=[Length(min=8, max=30)])
     firstname = StringField('First name : ', validators=[InputRequired(), Length(min=2, max=30)])
     lastname = StringField('Last name : ', validators=[InputRequired(), Length(min=2, max=30)])
     submit = SubmitField('Register')


class LoginForm ( FlaskForm):
    email = StringField('Email : ', validators=[Email(message="Please fil in a valide email address !"),
                                                InputRequired(),
                                                Length(min=5, max=120)])
    password = PasswordField('Password : ', validators=[Length(min=8, max=30)])
    submit = SubmitField('Log in')

