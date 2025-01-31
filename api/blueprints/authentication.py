"""
The Blueprint for routes used when for authenticating the user,
including register, login, logout and unregister routes.
"""

from api.config import year
from flask import flash, Blueprint, request, session
from flask import render_template, url_for, redirect
from models.user import User
from flask_login import current_user, login_required, login_user, logout_user


auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Allow the user to login.

    Response:
        HTML for login page on get request and redirect to home
        page on successful login.
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


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Allows the user to register to the site and saves their information
    to the database.

    Response:
        HTML for registration page on get request and redirect to login
        page on successful registration.
    """
    if current_user.is_authenticated:
        flash("You are already registed and logged in")
        return redirect(url_for('dash.home'))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            flash("Please fill all fields")
            return redirect(url_for('auth.register'))

        username.strip()
        email.strip()
        password.strip()
        confirm_password.strip()

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('auth.register'))

        if User.getByUsername(username):
            flash("Username already in use. Please choose another username.")
            return redirect(url_for('auth.register'))

        if User.getByEmail(email):
            flash("Email already in use. Please choose another email.")
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email, password=password)
        if user:
            user.save()
            flash("Registration successful!")
            return redirect(url_for('auth.login'))
        else:
            flash("Registration failed!")
            return redirect(url_for('auth.register'))

    else:
        return render_template(
            'register.html', title="Registration", year=year
        )


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Allows the user to logout of the site and clear user session
    data.

    Response:
        Redirect to index page on successful logout or login if
        user not logged in.
    """
    if current_user.is_authenticated:
        logout_user()
        session.clear()
        flash("Logout Successful!")
        return redirect(url_for("info.index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for('auth.login'))


@login_required
@auth_bp.route("/unregister", methods=["GET", "POST"])
def unregister():
    """
    Allows the user to delete their account from the website.

    Response:
        Redirect to index page on successful logout .
    """
    # TODO Also delete all user results when account is deleted
    if current_user.is_authenticated:
        temp_id = current_user.id
        logout_user()
        session.clear()
        User.deleteByID(temp_id)
        if User.getByID(temp_id):
            flash(
                "Account deletion unsuccesful! Please contact Administrator."
            )
            return redirect(url_for("info.index"))
        else:
            flash("Successfully deleted account!")
            return redirect(url_for("info.index"))
    else:
        return redirect(url_for('info.index'))
