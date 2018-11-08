from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config.from_envvar('IEEE_APP_CONFIG_FILE')

SQLAlchemy(app)
CORS(app)

db = app.extensions.get('sqlalchemy').db
session = db.session
Base = db.Model
