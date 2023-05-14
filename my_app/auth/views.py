from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user,logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from my_app import db
from my_app.models import User
from my_app.auth import auth
from my_app.auth.forms import LoginForm, RegisterForm

"""" ********************
     Controller : authentication
     *********************
"""
@auth.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password_hash = generate_password_hash(password, "sha256")

        new_user = User(email,password_hash,firstname,lastname,username)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration succeeded ! You can now log in...", "Success")

        return redirect(url_for('auth.login'))

    return render_template("auth/register.html", form=form, current_user=None)


@auth.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.list_riddle'))

    #if request.method == "GET":
    #    session['next'] = request.args.get('next')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("This email address doesn\'t exist !", "Danger")
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, form.password.data):
            flash("The password is incorrect", "Danger")
            return redirect(url_for('auth.login'))

        if user.blocked:
            flash("Your account has been blocked by an administrator.", "Danger")
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        return redirect(url_for('main.list_riddle'))

    return render_template('auth/login.html', form=form, current_user=None)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/list_users',methods=['GET'])
@login_required
def list_users():
    page = request.args.get('page', 1, type=int)
    logged_user=User.query.filter_by(id=current_user.id).first()
    if (not logged_user.admin):
        flash('You must be administrator to display this page', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    pagination = User.query.paginate(page=page, per_page=5)
    users = pagination.items
    return render_template('auth/users.html',users = users,pagination = pagination)

@auth.route('/setadmin',methods=['GET'])
@login_required
def setadmin():
    logged_user = User.query.filter_by(id=current_user.id).first()
    if (not logged_user.admin):
        flash('You must be administrator to manage users', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    user_id = request.args.get('user_id')
    action = request.args.get('action')
    managed_user = User.query.filter_by(id=user_id).first()

    if (action == 'promote'):
        managed_user.admin=True
    else:
        managed_user.admin=False

    db.session.add(managed_user)
    db.session.commit()

    return redirect(url_for('auth.list_users'))

@auth.route('/setblocked',methods=['GET'])
@login_required
def setblocked():
    logged_user = User.query.filter_by(id=current_user.id).first()
    if (not logged_user.admin):
        flash('You must be administrator to manage users', 'Danger')
        logout_user()
        return redirect(url_for('auth.login'))

    user_id = request.args.get('user_id')
    action = request.args.get('action')
    managed_user = User.query.filter_by(id=user_id).first()

    if (action == 'block'):
        managed_user.blocked=True
    else:
        managed_user.blocked=False

    db.session.add(managed_user)
    db.session.commit()

    return redirect(url_for('auth.list_users'))
