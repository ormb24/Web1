from my_app import app, db
from flask import render_template, redirect, url_for
from my_app.forms import PasswordForm, LoginForm
from my_app.models import User
from flask_login import login_required

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed'

@app.route('/toto')
def toto():
    result = User.query.filter_by(username='olivier').first().check_password('bonjour')
    return "bonjour %s" % result

@app.route('/liste', methods=['GET','POST'])
def login_password():
    form = PasswordForm()
    if form.validate_on_submit():
        # Pour les besoins de l'exercice, on utilisera le mot de passe associé à l'utilisateur 'olivier' pour se logger..
        # ... au lieu de 'hardcoder' le mot de passe dans le code Python.
        user = User.query.filter_by(username='olivier').first()
        if user is not None:
            if user.check_password(form.password.data):
                return "Bravo, le mot de passe %s est validé" % password
    return render_template('login_form.html', form=form)

@app.route('/kamoulox', methods=['GET','POST'])
def create_enigmas():
    return render_template('create_enigma.html', form=form)













password = 'pbkdf2:sha256:260000$0GvFMplE$716898ae3aba1bf8791864a6191150ceb4cff407dd46235e7b53dee295cd6be1'

enigmes = {}
enigmes['id1'] = {'question': 'Quel est le nom du cheval d\'Alexandre ?', 'reponse': 'Bucéphale'}
enigmes['id2'] = {'question': 'Quel est le nom du deuxième homme à avoir marché sur la lune ?', 'reponse': 'Aldrin'}
enigmes['id3'] = {'question': 'Quel est le nom du premier empereur romain ?', 'reponse': 'Auguste'}
enigmes['id4'] = {'question': 'Quel est le nom de l\'auteur qui a décrit les 3 lois de la robotique en S-F ?', 'reponse': 'Asimov'}
enigmes['id5'] = {'question': 'Quelle est la formule chimique de l\'acide sulfurique ?', 'reponse': 'H2SO4'}

id = 6

@app.route("/test")
def test():
    message = app.config['SQLALCHEMY_DATABASE_URI']
    message = password
    return message




