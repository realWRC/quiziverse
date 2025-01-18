#!/usr/bin/env python3
import json
import re
from api.config import app, login_manager, year, domain

from api.blueprints.information import info_bp
from api.blueprints.authentication import auth_bp
from api.blueprints.dashboard import dash_bp
from api.blueprints.quiz_routes import quiz_bp
from api.blueprints.answering_quiz import taking_bp
from api.blueprints.resultsblueprint import results_bp
from api.blueprints.apiroutes import api_db

from datetime import datetime, timezone, timedelta
from flask import flash, request, session, render_template, url_for, redirect, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from math import ceil
from models.result import Result
from models.user import User
from models.quiz import Quiz
from models import quizzesCollection, resultsCollection
from urllib.parse import urlparse
from pprint import pprint


@login_manager.user_loader
def load_user(user_id):
    """ Flask login user loader
    """
    return User.getByID(user_id)

app.register_blueprint(auth_bp)
app.register_blueprint(api_db)
app.register_blueprint(info_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(taking_bp)
app.register_blueprint(results_bp)

if __name__ == "__main__":
    app.run(debug=True)
