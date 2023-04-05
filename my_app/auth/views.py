from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        session['next'] = request.args.get('next')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = session.get('next')
            #return "La page était : %s" % next
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash("Nom d\'utilisateur ou mot de passe incorrect !")
    return render_template('auth/login.html', form=form)
