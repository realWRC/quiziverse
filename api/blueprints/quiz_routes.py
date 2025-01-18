import json
import re
from api.config import login_manager, year, domain

from api.blueprints.information import info_bp
from api.blueprints.authentication import auth_bp
from api.blueprints.dashboard import dash_bp

from datetime import datetime, timezone, timedelta
from flask import Blueprint, flash, request, session, render_template, url_for, redirect, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from math import ceil
from models.result import Result
from models.user import User
from models.quiz import Quiz
from models import quizzesCollection, resultsCollection
from urllib.parse import urlparse
from pprint import pprint


quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route("/create", methods=["GET", "POST"])
def create():
    """ Route for creating quizzes
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        data = request.form.get("quiz_json", '')
        pprint(data)
        data = json.loads(data)

        if data['time_limit'] is None:
            data['time_limit'] = 0

        validation = Quiz.validateFields(
            title = data['title'],
            description = data['description'],
            time_limit = data['time_limit'],
            category = data['category'],
        )
        if validation[0]:
            pass
        else:
            flash(validation[1])
            return render_template("create.html", title='quiz.create', year=year, data=data)

        # i = 0
        # pprint(data["questions"])
        # print(f"length of questions list {len(data['questions'])}")
        for question in data["questions"]:
            validation = Quiz.validateQuestion(question)
            # print(f"index {i} = {question}")
            if validation[0]:
                # print(f"index {i} = {quest}")
                # quiz.addQuestion(
                #     question = quest["question"],
                #     options = quest["options"],
                #     answer = quest["answer"],
                #     score = quest["score"],
                # )
                # pprint(quiz.__dict__)
                # i += 1
                pass
            else:
                flash(validation[1])
                return render_template("create.html", title='quiz.create', year=year, data=data)

        quiz = Quiz(
            title = data['title'],
            creator_id = current_user.get_id(),
            description = data['description'],
            time_limit = data['time_limit']
        )
        quiz.addMultipleQuestions(data['questions'])
        pprint(quiz.__dict__)
        quiz.save()
        flash("Quiz created successfully")
        return redirect(url_for('dash.home'))

    return render_template("create.html", title='quiz.create', year=year)
