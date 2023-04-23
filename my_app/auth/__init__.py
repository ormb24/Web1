from flask import Blueprint

auth = Blueprint('auth', __name__)

from my_app.auth import views
