## INFO ##
## INFO ##

# TODO: Put all dependencies to a virtualenv

# Import flask modules
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
