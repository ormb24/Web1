from flask import render_template, session, redirect, url_for, request, flash
from . import main
from flask_login import login_required
from .forms import CreateEnigmaForm
from .. import db
from ..models import Enigma

@main.route('/')
def index():
    return list_enigmas()

@main.route('/infos')
def infos():
    return render_template('main/infos.html')

@main.route('/liste')
@login_required
def list_enigmas():
    enigmas = Enigma.query.all()
    #return 'Liste des énigmes'
    return render_template('main/list_enigma.html', enigmas=enigmas)

@main.route('/kamoulox', methods=['GET','POST'])
@login_required
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

@main.route('/level', methods=['GET'])
@login_required
def update_level():
    id = request.args.get("id")
    enigma = Enigma.query.filter_by(id=id).first()
    if request.args.get("direction") == 'up':
        enigma.set_level(enigma.level +1)
    elif enigma.level > 0:
         enigma.set_level(enigma.level -1)
    else:
        flash("Le niveau ne peut être inférieur à 0 !")
    db.session.commit()
    return list_enigmas()






