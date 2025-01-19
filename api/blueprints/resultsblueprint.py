"""
The Blueprint for routes used when interacting with results.
The only route included being the resultinfo route
"""

from flask import Blueprint, flash, render_template, url_for, redirect
from flask_login import current_user
from models.result import Result
from models.quiz import Quiz
from models import resultsCollection


results_bp = Blueprint('results_bp', __name__)


@results_bp.route('/resultinfo/<quiz_id>', methods=["GET"])
def resultinfo(quiz_id):
    """
    Renders detailed results information for a given quiz taken
    by a user. The user is determined internally.

    Args:
        quiz_id(str): Unique identifier of a quiz.

    Response:
        HTML page created with the resultinfo.html template.
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    if not Quiz.get(quiz_id):
        flash("The quiz does not exist")
        return redirect(url_for('index'))

    if not Result.check(current_user.get_id(), quiz_id):
        flash("You have not taken a quiz on this site.")
        return redirect(url_for('index'))

    result = resultsCollection.find_one({
        "user_id": current_user.get_id(), "quiz_id": quiz_id
    })

    return render_template("resultinfo.html", result=result)
