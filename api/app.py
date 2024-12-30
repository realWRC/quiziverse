#!/usr/bin/env python3
from config import app, login_manager
from flask import flash, request, session, render_template
from flask_login import current_user, login_required, login_user, logout_user
from models.user import User


@login_manager.user_loader
def load_user(user_id):
    """ Flask login user loader
    """
    return User.getByID(user_id)


@app.route("/")
def index():
    """ Welcome Page
    """
    return render_template("index.html")


@app.route("/home/<username>")
def home():
    """ Renders the users home page
    """
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Registration route
    """
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            flash("Please fill all fields.")
            return render_template("register.html"), 400

        username.strip()
        email.strip()
        password.strip()
        confirm_password.strip()

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html"), 400

        if User.getByUsername(username):
            flash("Username already in use. Please choose another username.")
            return render_template("register.html"), 400

        if User.getByEmail(email):
            flash("Email already in use. Please choose another email.")
            return render_template("register.html"), 400

        user = User(username=username, email=email, password=password)
        if user:
            user.save()
            flash("Registration successful!")
            return render_template("login.html"), 201
        else:
            flash("Registration failed!")
            return render_template("register.html"), 500

    else:
        return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login route
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.")
            return render_template("login.html"), 400

        username.strip()
        password.strip()

        user = User.getByUsername(username)
        if not user:
            flash("Invalid username")
            return render_template("login.html"), 400

        if user.checkpwd(password):
            login_user(user)
            flash("Logged in successfully!")
            return render_template("home.html"), 200
        else:
            flash("Invalid user credentials.")
            return render_template("login.html"), 400
    else:
        return render_template("login.html")


@app.route("/unregister")
@login_required
def unregister():
    temp_id = current_user.id
    logout_user()
    session.clear()
    User.deleteByID(temp_id)
    if User.getByID(temp_id):
        flash("Account deletion unsuccesful! Please contact Administrator.")
        return render_template("index.html"), 400
    else:
        flash("Successfully deleted account!")
        return render_template("index.html"), 200


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    """ Logout route
    """
    flash("Logged out successfully!")
    return render_template("index.html"), 200


if __name__ == "__main__":
    app.run(debug = True)
