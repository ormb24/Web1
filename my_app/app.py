import random
from flask import Flask, redirect
from flask import request
from flask import render_template
from jinja2 import Template
from jinja2 import Environment, PackageLoader
from jinja2 import environment

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True

#env = Environment(loader=PackageLoader(__name__, 'templates'))



