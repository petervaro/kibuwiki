## INFO ##
## INFO ##

# TODO: Put all dependencies to a virtualenv

# Import python modules
import os.path

# Import flask modules
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager

# Import kibuwiki modules
from config import basedir
from kibuwiki import views, models

#------------------------------------------------------------------------------#
# Setup flask
app = Flask(__name__)
app.config.from_object('config')

# Create database
database = SQLAlchemy(app)

# Setup login and authentication
login_manager = LoginManager()
login_manager.init_app(app)
open_id = OpenID(app, os.path.join(basedir, 'tmp'))
