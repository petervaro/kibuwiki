## INFO ##
## INFO ##

# TODO: Put all dependencies to a virtualenv

# Import python modules
import os.path

# Import flask modules
from flask import Flask
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

# Import kibuwiki modules
from config import KIBUWIKI_BASEDIR

#------------------------------------------------------------------------------#
# Setup flask
app = Flask(__name__)
app.config.from_object('config')

# Create database
database = SQLAlchemy(app)

# Setup login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Setup authentication
open_id = OpenID(app, os.path.join(KIBUWIKI_BASEDIR, 'tmp'))

#------------------------------------------------------------------------------#
# Import kibuwiki modules
from kibuwiki import views, models
