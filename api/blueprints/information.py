
from flask import flash, render_template, url_for, redirect
from flask_login import current_user
from models.user import User
from flask import Blueprint, render_template
from api.config import year


info_bp = Blueprint('info', __name__)


@info_bp.route("/", methods=["GET", "POST"])
def index():
    """ Welcome Page
    """
    return render_template("index.html", title="QUIZIVERSE", year=year)


@info_bp.route("/about", methods=["GET"])
def about():
    """ About page
    """
    return render_template("about.html", title="ABOUT", year=year)


@info_bp.route("/account", methods=["GET", "POST"])
def account():
    """ Renders the users profile
    """
    if not current_user.is_authenticated:
        flash("You are are not logged in")
        return redirect(url_for('dash.home'))

    user = User.getByID(current_user.get_id())

    return render_template(
        "account.html",
        title="PROFILE",
        year=year, user=user
    )
