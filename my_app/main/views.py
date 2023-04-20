from flask import render_template, session, redirect, url_for, request, flash, abort

import my_app
from . import main
from flask_login import login_required, current_user, logout_user
from .forms import CreateEnigmaForm, RiddleForm
from .. import db
from ..models import Enigma, Riddle

@main.route('/')
def index():
    return infos()

@main.route('/infos')
def infos():
    return render_template('main/infos.html')

@main.route('/liste', methods=['GET','POST'])
@login_required
def list_enigmas():
    page = request.args.get('page',1,type=int)
    pagination = Enigma.query.order_by(Enigma.id.asc()).paginate(page=page,per_page=5)
    enigmas = pagination.items
    return render_template('main/list_enigma.html',enigmas=enigmas, pagination=pagination)
    ##enigmas = Enigma.query.all()
    #return 'Liste des énigmes'
    ##return render_template('main/list_enigma.html', enigmas=enigmas)

@main.route('/kamoulox', methods=['GET','POST'])
@login_required
def create_enigmas():
    #if request.method == "GET":
    #    session['next'] = request.args.get('next')

    isError=False
    form = CreateEnigmaForm()

    if request.method == "POST":
        if form.validate_on_submit():
            #return "Enigme : {}; Reponse : {}, Level : {}".format(enigma,response,level)
            try:
                enigma=Enigma(form.enigma.data, form.response.data, int(form.level.data))
                db.session.add(enigma)
                db.session.commit()
            except BaseException as e:
                isError=True
                flash('Un problème est survenu lors de l\'insertion dans la base de données : '+str(e))

            #next = session.get('next')
            #if next is None or not next.startswith('/'):
            #    next = url_for('main.index')
            #return redirect(next)
        else:
            isError=True

        if not isError:
            flash('Enigme ajoutée avec succès')
        else:
            flash("L\'ajout de l\'enigme a échoué !")
            #return render_template('main/create_enigma.html', form=form)
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

""" ********************
    Controller : Riddles
    ********************
"""
@main.route('/list_riddle', methods=['GET','POST'])
@login_required
def list_riddle():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    req_id = request.args.get('id')

    if req_id:
        if (int(req_id) != int(current_user.id) and not current_user.admin):
            abort(403)
        user_id = req_id
    else:
        user_id = current_user.id

    riddles = Riddle.query.order_by(Riddle.user_id == user_id)
    return render_template('main/list_riddle.html', riddles=riddles, user_id=int(user_id), current_user=current_user)

@main.route('/create_riddle', methods=['GET','POST'])
@login_required
def create_riddle():
    form = RiddleForm()
    form.id.data = 0
    return render_template("main/create_riddle.html",form=form, current_user=current_user, action="Create")

@main.route('/update_riddle', methods=['GET'])
@login_required
def update_riddle():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    id = request.args.get('id')
    riddle = Riddle.query.filter_by(id=id).first()

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)

    form = RiddleForm()

    form.id.data = riddle.id
    form.riddle.data = riddle.riddle
    form.answer.data = riddle.answer
    form.level.data = riddle.level

    return render_template("main/create_riddle.html", form=form, current_user=current_user, action="Update")

@main.route('/save_riddle',methods=['POST'])
@login_required
def save_riddle():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    form = RiddleForm()

    id = int(form.id.data)
    riddle = form.riddle.data
    answer = form.answer.data
    level = int(form.level.data)

    if id != 0:
        riddle_record = Riddle.query.filter_by(id=id).first()
        user_id = riddle_record.user_id
        message = "L'énigme a été modifiée !"
        action = "Update"
    else:
        riddle_record = Riddle(riddle,answer,level,current_user.id)
        message = "L'énigme a été créée !"
        action = "Create"

    if form.validate_on_submit():
        riddle_record.riddle = riddle
        riddle_record.answer = answer
        riddle_record.level = level
        db.session.add(riddle_record)
        db.session.commit()
        flash(message, 'Success')
        return redirect(url_for('main.create_riddle')) #To avoid re-submitting a post request on 'Refresh page'.
    else:
        return render_template("main/create_riddle.html",form=form, current_user=current_user, action=action)


@main.route('/delete_riddle', methods=['GET'])
def delete_riddle():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    id = request.args.get('id')
    user_id = request.args.get('user_id')
    riddle = Riddle.query.filter_by(id=id).first()

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)

    try:
        db.session.delete(riddle)
        db.session.commit()
    except BaseException as e:
        flash("L'énigme n'a pas été supprimée : "+ str(e))

    return redirect('/?id='+str(user_id), code=302)


