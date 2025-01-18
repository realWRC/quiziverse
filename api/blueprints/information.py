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

