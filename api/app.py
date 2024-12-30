#!/usr/bin/env python3
from api.config.config import app, login_manager
from flask import flash, jsonify, request, session, render_template
from flask_login import current_user, login_required, login_user, logout_user
from models.user import User


@login_manager.user_loader
def load_user(user_id):
    """ Flask login user loader
    """
    return User.getByID(user_id)


@app.route("/")
def home():
    """ Welcome Page
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
            return render_template("login.html")
    else:
        return render_template('register.html')


@app.route("/login", methods=["POST"])
def login():
    """ Login route
    """
    data = request.json

    if not data:
        return jsonify({
            "message": "Empty request"
        }), 400

    if not all(field in data for field in \
            ['username', 'password']):
        return jsonify({
            "message": "Please provide username and password."
        }), 400

    if not all(isinstance(data[field], str) for \
            field in ['username', 'password']):
        return jsonify({
            "message": "All fields are required and must be strings."
        }), 400

    username = data["username"].strip()
    password = data["password"].strip()

    user = User.getByUsername(username)
    if not user:
        return jsonify({
            "message": "Invalid username"
        }), 400

    if user.checkpwd(password):
        login_user(user)
        return jsonify({
            "message": "Logged in successfully!"
        }), 200
    else:
        return jsonify({
            "message": "Invalid user credentials."
        }), 400


@app.route("/unregister")
@login_required
def unregister():
    temp_id = current_user.id
    logout_user()
    session.clear()
    User.deleteByID(temp_id)
    if User.getByID(temp_id):
        return jsonify({
            "message": "Account deletion unsuccesful! Please contact Administrator."
        }), 400
    else:
        return jsonify({
            "message": "Successfully deleted account!"
        }), 200


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    """ Logout route
    """
    return jsonify({
        "message": "Logged out successfully!"
    }), 200


if __name__ == "__main__":
    app.run(debug = True)
