from flask import Flask
from os import environ
from flask_login import LoginManager
from flask_session import Session
from datetime import date, timedelta
from models import client
from models import quizzesCollection
from pymongo import ASCENDING

app = Flask(__name__)
app.secret_key = environ.get('SECRET')

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = client
app.config['SESSION_MONGODB_DB'] = 'quiziverse'
app.config['SESSION_MONGODB_COLLECTION'] = 'sessions'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

domain = "quiziverse.com"
year = date.today().strftime("%Y")

quizzesCollection.create_index([("created_at", ASCENDING)], name="created_at_idx")
quizzesCollection.create_index([("updated_at", ASCENDING)], name="updated_at_idx")
quizzesCollection.create_index([("title", ASCENDING)], name="title_idx")

