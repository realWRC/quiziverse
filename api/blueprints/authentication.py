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


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """ Registration route
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
        return render_template('register.html', title="Registration", year=year)
