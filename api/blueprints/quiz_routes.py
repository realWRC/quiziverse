import json
from api.config import year, domain
from flask import Blueprint, flash, request, session, render_template, url_for, redirect
from flask_login import current_user
from models.quiz import Quiz
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

        for question in data["questions"]:
            validation = Quiz.validateQuestion(question)
            if validation[0]:
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


@quiz_bp.route('/edit/<quiz_id>', methods=['GET', 'POST'])
def edit(quiz_id):
    """ Route for editing a users quiz if they are the creator
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))


    quiz = Quiz.get(quiz_id)

    if not quiz:
        flash("Invalid quiz id")
        return redirect(url_for('dash.home'))

    if not quiz['creator_id'] == current_user.get_id():
        flash("Not authorized to edit this quiz")
        return redirect(url_for('dash.home'))

    if request.method == "POST":
        data = request.form.get("quiz_json", '')

        session['edit_quiz_data'] = data

        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            flash("Invalid quiz data")
            return redirect(url_for('quiz.edit', quiz_id=quiz_id))

        if data['time_limit'] is None:
            data['time_limit'] = 0
        pprint(data)

        validation = Quiz.validateFields(
            title = data['title'],
            description = data['description'],
            category = data['category'],
            time_limit = data['time_limit'],
        )
        if validation[0]:
            pass
        else:
            flash(validation[1])
            return redirect(url_for('quiz.edit', quiz_id=quiz_id))

        for question in data["questions"]:
            validation = Quiz.validateQuestion(question)
            if validation[0]:
                pass
            else:
                session['edit_quiz_data'] = data
                flash(validation[1])
                return redirect(url_for('quiz.edit', quiz_id=quiz_id))

        try:
            Quiz.update(quiz_id, data)
            del session['edit_quiz_data']
            flash("Quiz updated successfully")
        except KeyError as e:
            print(e)
            flash("Quiz update failed")
        return redirect(url_for('dash.home'))

    try:
        data = session["edit_quiz_data"]
    except KeyError:
        data = None
        pass
    url = urlparse(request.referrer) 
    if (url.netloc == '127.0.0.1:5000' or url.netloc == domain) and url.path == f'/edit/{quiz_id}' and data:
        data['quiz_id'] = quiz_id
        return render_template("edit.html", title='quiz.edit', year=year, data=data)

    return render_template("edit.html", title='quiz.edit', year=year, data=quiz)


@quiz_bp.route('/delete/<quiz_id>', methods=['GET'])
def delete(quiz_id):
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        flash("Quiz not found")
        return redirect(request.referrer)

    if not quiz['creator_id'] == current_user.get_id():
        flash("You are not authorized to delete this quiz")
        return redirect(url_for('dash.home'))

    try:
        Quiz.delete(quiz_id)
        flash("Quiz deleted successfully")
        return redirect(request.referrer)
    except KeyError as e:
        print(e)
        flash("Quiz deletion failed")
    return redirect(request.referrer)
