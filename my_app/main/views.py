from flask import render_template, session, redirect, url_for, request, flash
from . import main
from flask_login import login_required
from .forms import CreateEnigmaForm
from .. import db
from ..models import Enigma

@main.route('/')
def index():
    return "Bienvenue sur la page d'accueil !"

@main.route('/liste')
@login_required
def list_enigmas():
    enigmas = Enigma.query.all()
    #return 'Liste des énigmes'
    return render_template('main/list_enigma.html', enigmas=enigmas)

@main.route('/kamoulox', methods=['GET','POST'])
#@login_required
def create_enigmas():
    if request.method == "GET":
        session['next'] = request.args.get('next')

    form = CreateEnigmaForm()
    if form.validate_on_submit():
        #return "Enigme : {}; Reponse : {}, Level : {}".format(enigma,response,level)
        enigma=Enigma(form.enigma.data, form.response.data, int(form.level.data))
        db.session.add(enigma)
        db.session.commit()
        flash('Enigme ajoutée avec succès')

        next = session.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main.index')
        return redirect(next)
    else:
        return render_template('main/create_enigma.html', form=form)





enigmes = {}
enigmes['id1'] = {'question': 'Quel est le nom du cheval d\'Alexandre ?', 'reponse': 'Bucéphale'}
enigmes['id2'] = {'question': 'Quel est le nom du deuxième homme à avoir marché sur la lune ?', 'reponse': 'Aldrin'}
enigmes['id3'] = {'question': 'Quel est le nom du premier empereur romain ?', 'reponse': 'Auguste'}
enigmes['id4'] = {'question': 'Quel est le nom de l\'auteur qui a décrit les 3 lois de la robotique en S-F ?', 'reponse': 'Asimov'}
enigmes['id5'] = {'question': 'Quelle est la formule chimique de l\'acide sulfurique ?', 'reponse': 'H2SO4'}

id = 6





