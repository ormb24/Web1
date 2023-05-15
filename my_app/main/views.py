from flask import render_template, redirect, url_for, request, flash, abort, jsonify,json
from flask import current_app
from flask_login import login_required, current_user, logout_user

from my_app.main import main
from my_app.main.forms import RiddleForm, ClueForm
from my_app import db
from my_app.models import Riddle, Clue, User

@main.route('/')
@login_required
def index():
    return list_riddle()
@main.route('/infos')
def infos():
    return render_template('main/infos.html')

@main.route('/liste', methods=['GET','POST'])
@login_required
def liste():
    return list_riddle()

""" *******************
    Controller : Riddle
    *******************
"""
@main.route('/list_riddle', methods=['GET'])
@login_required
def list_riddle():
    page = request.args.get('page', 1, type=int)
    validate_user();

    if current_user.admin:
        pagination = Riddle.query.paginate(page=page, per_page=5)
    else:
        pagination = Riddle.query.filter(Riddle.user_id == current_user.id).paginate(page=page, per_page=5)

    riddles = pagination.items
    return render_template('main/list_riddle.html', riddles=riddles, current_user=current_user, pagination=pagination)

@main.route('/list_riddle_ajax',methods=['GET','POST'])
@login_required
def list_riddle_ajax():
    page = request.args.get('page', 1, type=int)
    validate_user();

    if current_user.admin:
        pagination = Riddle.query.paginate(page=page, per_page=5)
    else:
        pagination = Riddle.query.filter(Riddle.user_id == current_user.id).paginate(page=page, per_page=5)

    riddles = pagination.items
    return jsonify(riddles)

@main.route('/create_riddle', methods=['GET','POST'])
@login_required
def create_riddle():
    validate_user();
    form = RiddleForm()
    form.id.data = 0
    return render_template("main/create_riddle.html",form=form, current_user=current_user, action="Create")

@main.route('/update_riddle', methods=['GET'])
@login_required
def update_riddle():
    validate_user();

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
    validate_user();

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
    validate_user();

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
    validate_user()

    riddle_id = request.args.get("riddle_id")
    direction = request.args.get("direction")
    level_min = current_app.config['LEVEL_MIN']
    level_max = current_app.config['LEVEL_MAX']


    logged_user = User.query.filter_by(id=current_user.id).first()
    riddle = Riddle.query.filter_by(id=riddle_id).first()

    if not(logged_user.admin or riddle.user_id == current_user.id):
        flash("Vous n'êtes pas autorisé à modifier cette énigme !", "Danger")
        #abort(403)
        return redirect("/liste")

    if (direction == 'up'):
        if (riddle.level< level_max):
            riddle.set_level(riddle.level + 1)
    else:
        if (riddle.level > level_min):
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
    validate_user();


@main.route('/clue', methods=['GET'])
@login_required
def clue():
    validate_user();

    riddle_id = request.args.get('riddle_id')
    clue_id= request.args.get('clue_id')
    clue = Clue.query.filter_by(id=clue_id).first()
    riddle = Riddle.query.filter_by(id=riddle_id).first()
    form = ClueForm()

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)

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

    return render_template(template, form=form)
@main.route('/update_clue', methods=['GET'])
@login_required
def update_clue():
    validate_user();
    return render_template("main/create_clue.html", form=form)

@main.route('/save_clue',methods=['POST'])
@login_required
def save_clue():
    validate_user();

    form = ClueForm()

    id = int(form.id.data)
    riddle_id=int(form.riddle_id.data)
    clue = form.clue.data

    if id != 0:
        clue_record = Clue.query.filter_by(id=id).first()
        message = "L'indice a été modifié !"
    else:
        clue_record = Clue(clue=clue,riddle_id=riddle_id)
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
    validate_user();

    riddle_id=request.args.get('riddle_id')
    clue_id=request.args.get('clue_id')
    clue = Clue.query.filter_by(id=clue_id).first()
    riddle = Riddle.query.filter_by(id=riddle_id).first()

    if not (current_user.admin) and not (riddle.user_id == current_user.id):
        abort(403)

    if clue:
        try:
            db.session.delete(clue)
            db.session.commit()
            #flash("L'indice a été supprimé !", "Success")
        except BaseException as e:
            flash("L'indice n'a pas été supprimé : "+ str(e),"Warning")
    else:
        flash("Il n'y pas d'indice pour cette énigme ! ", "Warning")

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

""" ********************
    Helper functions :
    ********************
"""
def validate_user():
    if current_user.blocked:
        flash('Your account has been blocked by an administrator.', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))
    else:
        return

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