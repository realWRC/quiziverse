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

taking_bp = Blueprint('taking', __name__)

@taking_bp.route('/quizinfo/<quiz_id>', methods=['GET'])
def quizinfo(quiz_id):
    """ Displays information about a quiz before it is taken
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        flash("Quiz not found")
        return redirect(request.referrer)

    return render_template('quizinfo.html', title=quiz['title'] , year=year, quiz=quiz)


@taking_bp.route('/take/<quiz_id>', methods=['GET'])
def takequiz(quiz_id):
    """ Allows user to take a quiz from.
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    quiz = Quiz.get(quiz_id)
    if quiz == None:
        flash("Quiz not found")
        return redirect(request.referrer)

    if not "taking_quiz" in session:
        start_time = datetime.now(timezone.utc)
        finish_time = start_time + timedelta(seconds=quiz["time_limit"])
        # This should cache without calling session.modified = True
        print("IN HERE")
        session["taking_quiz"] = {
            "quiz_id": quiz_id,
            "current_index": 0,
            "previous_index": None,
            "answers": {},
            "timeout": False,
            "finished": False,
            "start_time": start_time,
            "current_time": start_time,
            "finish_time": finish_time,
            "duration": finish_time - start_time
        }
        del start_time
        del finish_time

    # Potentially Bugged or useless
    if session["taking_quiz"]["quiz_id"] != quiz_id:
        flash("Use interface to take the quiz")
        del session["taking_quiz"]
        return redirect(url_for('dash.home'))

    # Consider changing to redis for session storage to get faster access times by caching quiz in session

    start_time = session["taking_quiz"]["start_time"]
    session["taking_quiz"]["duration"] = session["taking_quiz"]["finish_time"] - session["taking_quiz"]["current_time"]
    session.modified = True
    return render_template(
        'takequiz.html',
        title=quiz["title"],
        year=year,
        question=quiz['questions'][session["taking_quiz"]["current_index"]],
        start_time=start_time,
        duration=int((session["taking_quiz"]["duration"]).total_seconds())
    )


@taking_bp.route('/skip/<quiz_id>', methods=["POST"])
def skip(quiz_id):
    """ Skips a quiz question
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('dash.home'))

    session["taking_quiz"]["current_time"] = datetime.now(timezone.utc)

    quiz = Quiz.get(quiz_id)
    if quiz == None:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('dash.home'))

    if session["taking_quiz"]["current_time"] > session["taking_quiz"]["finish_time"]:
        session["taking_quiz"]["timeout"] = True
        flash("Time Ran Out")
        return redirect(url_for('taking.finishquiz', quiz_id=quiz_id))

    if session["taking_quiz"]["current_index"] == (len(quiz["questions"]) - 1):
        session["taking_quiz"]["finished"] = True
        return redirect(url_for('taking.finishquiz', quiz_id=quiz_id))

    payload = request.form.get('answer')
    if not payload:
        print("No data recied when submitting quiz")
        return redirect(request.referrer)

    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        del session["taking_quiz"]
        flash("Invalid data submitted")
        return redirect(request.referrer)

    question_id, answer = list(payload['answer'].items())[0]
    del payload
    if question_id != quiz["questions"][session["taking_quiz"]["current_index"]]["question_id"]:
        del session["taking_quiz"]
        flash("Tampering detected")
        return redirect(url_for('dash.home'))

    # answer = uuid4()
    answer = None
    session["taking_quiz"]["answers"][question_id] = {
        "question_id": question_id,
        "answer": answer
    }

    session["taking_quiz"]["previous_index"] = session["taking_quiz"]["current_index"]
    session["taking_quiz"]["current_index"] += 1 
    session.modified = True

    return redirect(url_for('taking.takequiz', quiz_id=quiz_id))


@taking_bp.route('/previous/<quiz_id>', methods=['POST'])
def previous(quiz_id):
    """ Handles going back ward in quiz
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('dash.home'))

    session["taking_quiz"]["current_time"] = datetime.now(timezone.utc)

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('dash.home'))

    if session["taking_quiz"]["current_time"] > session["taking_quiz"]["finish_time"]:
        session["taking_quiz"]["timeout"] = True
        flash("Time Ran Out")
        return redirect(url_for('taking.finishquiz', quiz_id=quiz_id))

    payload = request.form.get('answer')
    if not payload:
        print("No data recied when submitting quiz")
        return redirect(request.referrer)

    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        del session["taking_quiz"]
        flash("Invalid data submitted")
        return redirect(request.referrer)

    question_id, answer = list(payload['answer'].items())[0]
    del payload
    del answer
    if question_id != quiz["questions"][session["taking_quiz"]["current_index"]]["question_id"]:
        del session["taking_quiz"]
        flash("Tampering detected")
        return redirect(url_for('dash.home'))

    # Store answer
    if session["taking_quiz"]["current_index"] == 0:
        flash("No previous question to do back to")
        return redirect(url_for('taking.takequiz', quiz_id=quiz_id))

    session["taking_quiz"]["previous_index"] = session["taking_quiz"]["current_index"] - 1
    session["taking_quiz"]["current_index"] = session["taking_quiz"]["previous_index"]
    session.modified = True
    return redirect(url_for('taking.takequiz', quiz_id=quiz_id))


@taking_bp.route('/submitanswer/<quiz_id>', methods=["POST"])
def submitanswer(quiz_id):
    """ Handles Submittion of question answers
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('dash.home'))

    session["taking_quiz"]["current_time"] = datetime.now(timezone.utc)

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('dash.home'))

    if session["taking_quiz"]["current_time"] > session["taking_quiz"]["finish_time"]:
        session["taking_quiz"]["timeout"] = True
        flash("Time Ran Out")
        return redirect(url_for('taking.finishquiz', quiz_id=quiz_id))

    # if session["taking_quiz"]["current_index"] == 0 and session["taking_quiz"]["previous_index"] != None:
    #     flash("Quiz was temtered with")
    #     del session["taking_quiz"]
    #     return redirect(url_for('dash.home'))

    payload = request.form.get('answer')
    if not payload:
        print("No data recied when submitting quiz")
        return redirect(request.referrer)

    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        del session["taking_quiz"]
        flash("Invalid data submitted")
        return redirect(request.referrer)

    question_id, answer = list(payload['answer'].items())[0]
    del payload
    if question_id != quiz["questions"][session["taking_quiz"]["current_index"]]["question_id"]:
        del session["taking_quiz"]
        flash("Tampering detected")
        return redirect(url_for('dash.home'))

    # Store answer
    session["taking_quiz"]["answers"][question_id] = {
        "question_id": question_id,
        "answer": answer
    }

    if session["taking_quiz"]["current_index"] == (len(quiz["questions"]) - 1):
        session["taking_quiz"]["finished"] = True
        return redirect(url_for('taking.finishquiz', quiz_id=quiz_id))

    session["taking_quiz"]["previous_index"] = session["taking_quiz"]["current_index"]
    session["taking_quiz"]["current_index"] += 1
    session.modified = True

    return redirect(url_for('taking.takequiz', quiz_id=quiz_id))


@taking_bp.route('/quit/<quiz_id>', methods=['POST'])
def quit(quiz_id):
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('dash.home'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('dash.home'))

    if session["taking_quiz"]["quiz_id"] != quiz_id:
        print("Wrong quit url")
        return redirect(url_for(request.referrer, quiz_id=quiz_id))

    return redirect(url_for('taking.finishquiz', quiz_id=quiz_id))


@taking_bp.route('/finishquiz/<quiz_id>')
def finishquiz(quiz_id):
    """ Finishes quiz
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('dash.home'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('dash.home'))

    answers = session["taking_quiz"]["answers"]
    user_score = 0
    correct_answers = 0
    questions_attempted = 0
    questions_skiped = 0
    max_score = quiz["total_score"]
    if session["taking_quiz"]["timeout"]:
        heading = f"Quiz Timeout!"
    else:
        heading = f"Quiz Finished!"

    for question in quiz["questions"]:
        question_id = question["question_id"]
        if question_id in answers.keys():
            if answers[question_id]["answer"] != None:
                questions_attempted += 1
            else:
                questions_skiped += 1
            if question["answer"] == answers[question_id]["answer"]:
                user_score += question["score"]
                correct_answers += 1
    # try:
    #     accuracy = (correct_answers/questions_attempted) * 100
    # except ZeroDivisionError:
    #     accuracy = 0
    #     pass
    if correct_answers == 0 or questions_attempted == 0:
        accuracy = 0
    else:
        accuracy = (correct_answers/questions_attempted) * 100

    if max_score:
        percentage_score = (user_score/max_score) * 100
    else:
        percentage_score = 0

    quiz_results = {
        "title": quiz["title"],
        "percentage_score": percentage_score,
        "user_score": user_score,
        "correct_answers": correct_answers,
        "questions_attempted": questions_attempted,
        "accuracy": accuracy,
        "latest_attempt": datetime.now(timezone.utc)
    }

    if not Result.check(current_user.get_id(), quiz_id):
        result_document = Result(
            current_user.get_id(),
            quiz_id,
            **quiz_results
        )
        result_document.save()
        del result_document
    else:
        try:
            Result.update(current_user.get_id(), quiz_id, quiz_results)
            print("Update Called")
        except Exception as e:
            print(e)

    del session["taking_quiz"]

    return render_template(
        'finishquiz.html', year=year,
        title=quiz['title'],
        quiz_id=quiz["quiz_id"], 
        heading=heading, 
        percentage_score=percentage_score,
        user_score=user_score,
        correct_answers=correct_answers,
        questions_attempted=questions_attempted,
        max_score=max_score,
        accuracy=accuracy
    )

