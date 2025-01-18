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


app.register_blueprint(auth_bp)
app.register_blueprint(info_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(taking_bp)
app.register_blueprint(results_bp)


@login_manager.user_loader
def load_user(user_id):
    """ Flask login user loader
    """
    return User.getByID(user_id)


@app.route('/get', methods=['GET'])
def getAll():
    """ Gets all quizzes from database
    """
    page = int(request.args.get('page', 1))
    if page <= 0:
        page = 1

    per_page = int(request.args.get('per_page', 30))
    if per_page > 100:
        per_page = 100
    if per_page <= 0:
        per_page = 30

    skip = (page - 1) * per_page
    query = request.args.get('search', '')

    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    if pattern.search(query):
        query = re.escape(query)

    if query:
        total = quizzesCollection.count_documents(
            {"title": {"$regex": query, "$options": "i"}}
            )
        total_pages = ceil(total / per_page) if total > 0 else 1
        cursor = quizzesCollection.find(
            {"title": {"$regex": query, "$options": "i"}},
            {"_id": False, "creator_id": False},
            ).sort([("title", 1), ("updated_at", 1)]).skip(skip).limit(per_page)
        quizzes = list(cursor)
    else:
        total = quizzesCollection.count_documents({})
        total_pages = ceil(total / per_page) if total > 0 else 1
        # cursor = Quiz.getAll().skip(skip).sort("updated_at", 1).limit(per_page)
        cursor = quizzesCollection.find({}, {'_id': False, 'creator_id': False}).skip(skip).sort("updated_at", 1).limit(per_page)
        quizzes = list(cursor)

    if quizzes:
        return jsonify(quizzes)
    else:
        return jsonify({
            "message": "Not found"
        }), 500


@app.route('/get/<quiz_id>', methods=["GET"])
def get(quiz_id):
    """ Gets a quiz and returns it as json
    """
    cursor = quizzesCollection.find({"quiz_id": quiz_id}, {"_id": False, "creator_id": False})
    quiz = list(cursor)
    if not quiz:
        return jsonify({
            "message": "Quiz not found"
        }), 400

    return jsonify(quiz)


if __name__ == "__main__":
    app.run(debug=True)
