from api.config import year, domain
from flask import Blueprint, request, url_for, flash, redirect, render_template
from models.user import User
from flask_login import current_user, login_required, login_user, logout_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """ Login route
    """
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('dash.home'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.")
            return redirect(url_for('auth.login'))

        username.strip()
        password.strip()

        user = User.getByUsername(username)
        if not user:
            flash("Invalid username")
            return redirect(url_for("auth.login"))

        if user.checkpwd(password):
            login_user(user)
            # flash("Logged in successfully!")
            return redirect(url_for('dash.home'))
        else:
            flash("Invalid user credentials.")
            return redirect(url_for("auth.login"))
    else:
        return render_template("login.html", title="Login", year=year)
