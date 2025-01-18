from flask import Blueprint, render_template
from api.config import year

info_bp = Blueprint('info', __name__)

@info_bp.route("/about", methods=["GET"])
def about():
    """ About page
    """
    return render_template("about.html", title="ABOUT", year=year)
