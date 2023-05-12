from flask import render_template, redirect, url_for, request, flash, abort, jsonify, json
from flask_login import login_required, current_user, logout_user

from my_app.main import main
from my_app.main.forms import RiddleForm, ClueForm
from my_app import db
from my_app.models import Riddle, Clue, User, Category

@main.route('/')
@login_required
def index():
    return list_riddle()
@main.route('/infos')
def infos():
    return render_template('main/infos.html')

@main.route('/liste', methods=['GET','POST'])
@login_required
def list():
    return list_riddle()

""" *******************
    Controller : Riddle
    *******************
"""
@main.route('/list_riddle', methods=['GET'])
@login_required
def list_riddle():
    page = request.args.get('page', 1, type=int)
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    if current_user.admin:
        pagination = Riddle.query.paginate(page=page, per_page=5)
    else:
        pagination = Riddle.query.filter(Riddle.user_id == current_user.id).paginate(page=page, per_page=5)


    riddles = pagination.items
    num_list = []
    for i in pagination.iter_pages(left_edge = 3, right_edge=3, left_current=3, right_current=3):
        num_list.append(i)

    #return jsonify({'json_list': [i.serialize for i in pagination.itms], 'pages_lst':num_list})



    return render_template('main/list_riddle.html', riddles=riddles, current_user=current_user, pagination=pagination)

@main.route('/list_riddle_ajax',methods=['GET','POST'])
@login_required
def list_riddle_ajax():
    page = request.args.get('page', 1, type=int)
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    if current_user.admin:
        pagination = Riddle.query.paginate(page=page, per_page=5)
    else:
        pagination = Riddle.query.filter(Riddle.user_id == current_user.id).paginate(page=page, per_page=5)


    """
    pagination = Category.query.paginate(page=page, per_page=5)
    categories = pagination.items
    categories = Category.query.first()
    """
    riddles = pagination.items

    rep = riddles
    return jsonify(rep)

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

    id = request.args.get('riddle_id')
    riddle = Riddle.query.filter_by(id=id).first()

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)

    form = RiddleForm()

    if riddle:
        form.id.data = riddle.id
        form.riddle.data = riddle.riddle
        form.answer.data = riddle.answer
        form.level.data = riddle.level
    else:
        flash("Cette énigme n\'existe pas !", 'Danger')
        return redirect(url_for('main.list_riddle'))

    return render_template("main/create_riddle.html", form=form, current_user=current_user, action="Update")

@main.route('/save_riddle',methods=['POST'])
@login_required
def save_riddle():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    form = RiddleForm()
    action = "Create"

    if form.validate_on_submit():

        id = int(form.id.data)
        riddle = form.riddle.data
        answer = form.answer.data
        clue = form.clue.data
        level = int(form.level.data)

        # Créer ou mettre à jour l'énigme
        if id != 0:
            riddle_record = Riddle.query.filter_by(id=id).first()
            riddle_record.riddle = riddle
            riddle_record.answer = answer
            riddle_record.level = level
            action = "Update"
            message = "L'énigme a été modifiée !"
        else:
            riddles = Riddle.query.filter_by(riddle=riddle).first()
            action = "Create"
            # On supposera que l'énigme doit être unique pour tous les utilisateurs; sinon modifier le modèle pour la rendre unique par utilisateur.
            if riddles:
                flash("L\'énigme existe déjà en DB !", "Danger")
                return render_template("main/create_riddle.html", form=form, current_user=current_user, action=action)
            else:
                riddle_record = Riddle(riddle=riddle, answer=answer, level=level, user_id=current_user.id)
                action = "Create"
                message = "L'énigme a été créée !"

        db.session.add(riddle_record)

        #Créer ou mettre à jour l'indice
        if clue != '':
            clue_record = Clue(clue=clue, riddle=riddle_record)
            db.session.add(clue_record)

        db.session.commit()
        flash(message, 'Success')
        return redirect(url_for('main.create_riddle')) #To avoid re-submitting a post request on 'Refresh page'.
    else:
        return render_template("main/create_riddle.html",form=form, current_user=current_user, action=action)


@main.route('/delete_riddle', methods=['GET'])
@login_required
def delete_riddle():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    id = request.args.get('riddle_id')
    riddle = Riddle.query.filter_by(id=id).first()

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)
    try:
        db.session.delete(riddle)
        db.session.commit()

    except BaseException as e:
        flash("L'énigme n'a pas été supprimée : "+ str(e),"Warning")

    #return list_riddle()
    return list_riddle_ajax()

@main.route('/level', methods=['GET'])
@login_required
def level():
    id = request.args.get("riddle_id")

    riddle = Riddle.query.filter_by(id=id).first()

    if (request.args.get("direction") == 'up'):
        if (riddle.level<10):
            riddle.set_level(riddle.level + 1)
    else:
        if (riddle.level >0):
            riddle.set_level(riddle.level - 1)

    db.session.commit()
    return str(riddle.level)

""" ********************
    Controller : Clue
    ********************
"""
@main.route('/list_clues',methods=['GET'])
@login_required
def list_clues():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))


@main.route('/clue', methods=['GET'])
@login_required
def clue():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    riddle_id = request.args.get('riddle_id')
    clue = Clue.query.filter_by(riddle_id=riddle_id).first()
    riddle = Riddle.query.filter_by(id=riddle_id).first()
    form = ClueForm()

    if clue:
        template = "main/update_clue.html"
        form.id.data = clue.id
        form.clue.data = clue.clue
        form.riddle.data = clue.riddle.riddle
        form.riddle_id.data = riddle_id
    else:
        template = "main/create_clue.html"
        form.id.data = 0
        form.clue.data= ""
        form.riddle.data = riddle.riddle
        form.riddle_id.data = riddle_id

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)

    return render_template(template, form=form)
@main.route('/update_clue', methods=['GET'])
@login_required
def update_clue():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template("main/create_clue.html", form=form)

@main.route('/save_clue',methods=['POST'])
@login_required
def save_clue():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    form = ClueForm()

    id = int(form.id.data)
    riddle_id=int(form.riddle_id.data)
    clue = form.clue.data

    if id != 0:
        clue_record = Clue.query.filter_by(id=id).first()
        message = "L'indice a été modifié !"
    else:
        clue_record = Clue(clue,riddle_id)
        message = "L'indice a été créé !"

    if form.validate_on_submit():
        clue_record.clue = clue
        clue_record.riddle_id = riddle_id
        db.session.add(clue_record)
        db.session.commit()
        flash(message, 'Success')
        return redirect(url_for('main.list_riddle')) #To avoid re-submitting a post request on 'Refresh page'.
    else:
        return render_template("main/create_clue.html",form=form)

@main.route('/delete_clue', methods=['GET'])
@login_required
def delete_clue():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    riddle_id = request.args.get('riddle_id')
    clue = Clue.query.filter_by(riddle_id=riddle_id).first()
    riddle = Riddle.query.filter_by(id=riddle_id).first()

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)

    if clue:
        try:
            db.session.delete(clue)
            db.session.commit()
            flash("L'indice a été supprimé !", "Success")
        except BaseException as e:
            flash("L'indice n'a pas été supprimé : "+ str(e),"Warning")
    else:
        flash("Il n'y pas d'indice pour cette énigme ! ", "Warning")

    return list_riddle()




""" ********************
    Controller : Error Pages
    ********************
"""
@main.app_errorhandler(404)
def page_not_found(e):
     return render_template("errors/404.html"), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500