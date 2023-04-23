from flask import Blueprint

main = Blueprint('main', __name__)

from my_app.main import views