
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pathlib

BASE_DIR = pathlib.Path(__file__).parent

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./templates/static')


app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apteka.db'
app.secret_key = 'very hard secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

manager = LoginManager(app)
manager.login_view = 'log_page'

app.run(debug=True, use_reloader=True)

from . import routes , models

