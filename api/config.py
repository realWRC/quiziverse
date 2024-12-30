from flask import Flask
from os import environ
from flask_login import LoginManager
from flask_session import Session
from datetime import timedelta
from models import client

app = Flask(__name__)
app.secret_key = environ.get('SECRET')

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = client
app.config['SESSION_MONGODB_DB'] = 'quizziverse'
app.config['SESSION_MONGODB_COLLECTION'] = 'sessions'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
