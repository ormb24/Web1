from my_app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, render_template
import random

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

@app.route('/liste')
def login():
    return 'Hi'



