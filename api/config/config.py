from flask import Flask
from os import environ
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = environ.get('SECRET')

login_manager = LoginManager()
login_manager.init_app(app)
