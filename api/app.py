#!/usr/bin/env python3
from config.config import app, login_manager
from flask import jsonify, request, session
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
    return jsonify({
        "message": "Welcome to quizziverse",
    })


@app.route("/register", methods=["POST"])
def register():
    """ Registration route
    """
    data = request.json

    if not data:
        return jsonify({
            "message": "Empty request"
        }), 400

    if not all(field in data for field in \
            ['username', 'password', 'email','confirm_password']):
        return jsonify({
            "message": "All fields are required."
        }), 400

    if not all(isinstance(data[field], str) for \
            field in ['username', 'email', 'password', 'confirm_password']):
        return jsonify({
            "message": "All fields are required and must be strings."
        }), 400

    username = data["username"].strip()
    email = data["email"].strip()
    password = data["password"].strip()
    confirm_password = data["confirm_password"].strip()

    if password != confirm_password:
        return {
            "message": "Passwords do not match"
        }, 400

    if User.getByUsername(username):
        return {
            "message": "Username already in use. Please choose another username."
        }, 400

    if User.getByEmail(email):
        return {
            "message": "Email already in use. Please choose another email."
        }, 400

    user = User(username=username, email=email, password=password)
    user.save()

    return {
        "message": "Registration successful!"
    }, 201


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
    }), 201


if __name__ == "__main__":
    app.run(debug = True)
