from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from keycloak_adapter import sensitive_cache, public_cache
from keycloak_adapter.adapters.flask_adapter import FlaskPolicyEnforcerExtension

app = Flask(__name__)
app.config.from_envvar('IEEE_APP_CONFIG_FILE')

sensitive_cache.configure('dogpile.cache.null')
public_cache.configure('dogpile.cache.null')

SQLAlchemy(app)
CORS(app)
policy_enforcer = FlaskPolicyEnforcerExtension(app)

db = app.extensions.get('sqlalchemy').db
session = db.session
Base = db.Model
