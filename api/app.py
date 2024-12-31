#!/usr/bin/env python3
from api.config import app, login_manager
from datetime import date
from flask import flash, request, session, render_template, url_for, redirect
from flask_login import current_user, login_required, login_user, logout_user
from models.user import User
from pprint import pprint

year = date.today().strftime("%Y")


@login_manager.user_loader
def load_user(user_id):
    """ Flask login user loader
    """
    return User.getByID(user_id)


@app.route("/", methods=["GET", "POST"])
def index():
    """ Welcome Page
    """
    return render_template("index.html", title="QUIZIVERSE", year=year)


@app.route("/home", methods=["GET", "POST"])
def home():
    """ Renders the users home page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template("home.html", title="HOME", year=year)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    """ Renders the users profile
    """
    return render_template("profile.html", title="PROFILE", year=year)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Registration route
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            flash("Please fill all fields")
            return redirect(url_for('register'))

        username.strip()
        email.strip()
        password.strip()
        confirm_password.strip()

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('register'))

        if User.getByUsername(username):
            flash("Username already in use. Please choose another username.")
            return redirect(url_for('register'))

        if User.getByEmail(email):
            flash("Email already in use. Please choose another email.")
            return redirect(url_for('register'))

        user = User(username=username, email=email, password=password)
        if user:
            user.save()
            flash("Registration successful!")
            return redirect(url_for('login'))
        else:
            flash("Registration failed!")
            return redirect(url_for('register'))

    else:
        return render_template('register.html', title="Registration", year=year)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login route
    """
    if current_user.is_authenticated:
        return redirect(request.referrer)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.")
            return redirect(url_for("login"))

        username.strip()
        password.strip()

        user = User.getByUsername(username)
        if not user:
            flash("Invalid username")
            return redirect(url_for("login"))

        if user.checkpwd(password):
            login_user(user)
            # flash("Logged in successfully!")
            return redirect(url_for("home"))
        else:
            flash("Invalid user credentials.")
            return redirect(url_for("login"))
    else:
        return render_template("login.html", title="Login", year=year)


@login_required
@app.route("/unregister", methods=["GET", "POST"])
def unregister():
    if current_user.is_authenticated:
        temp_id = current_user.id
        logout_user()
        session.clear()
        User.deleteByID(temp_id)
        if User.getByID(temp_id):
            # flash("Account deletion unsuccesful! Please contact Administrator.")
            return redirect(url_for("index"))
        else:
            # flash("Successfully deleted account!")
            return render_template("index.html"), 200
    else:
        return redirect(url_for('index'))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """ Logout route
    """
    if current_user.is_authenticated:
        logout_user()
        session.clear()
        return redirect(url_for("index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for('login'))


@app.route("/create", methods=["GET", "POST"])
def create():
    """ Route for creating quizzes
    """
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        pprint(request.form.get("quiz_json"))

    return render_template("create.html", title="Create", year=year)


if __name__ == "__main__":
    app.run(debug=True)
