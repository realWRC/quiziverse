#!/usr/bin/env python3
import json
from api.config import app, login_manager
from datetime import date, datetime, timezone, timedelta
from flask import flash, request, session, render_template, url_for, redirect, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from models.result import Result
from models.user import User
from models.quiz import Quiz
from urllib.parse import urlparse
from uuid import uuid4
from pprint import pprint

year = date.today().strftime("%Y")
domain = "quiziverse.com"

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
        flash("You must be logged in first.")
        return redirect(url_for('login'))

    query = request.form.get('search', '')

    if query:
        quizzes = Quiz.search(query)
        # present = True if len(list(quizzes)) else False
    else:
        quizzes = Quiz.getAll()
    return render_template("home.html", title="HOME", year=year, query=query, quizzes=quizzes)

@app.route("/myquizzes")
def myquizzes():
    """ Shows all quizes created by a given user.
    """
    my_quizzes = Quiz.getByFilter({"creator_id": current_user.get_id()})
    my_quizzes = list(my_quizzes)
    return render_template("myquizzes.html", quizzes=my_quizzes, title="My Quizzes", year=year)


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
        flash("You are already registed and logged in")
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
        flash("You are already logged in.")
        return redirect(url_for('home'))

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
            flash("Account deletion unsuccesful! Please contact Administrator.")
            return redirect(url_for("index"))
        else:
            flash("Successfully deleted account!")
            return redirect(url_for("index"))
    else:
        return redirect(url_for('index'))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """ Logout route
    """
    if current_user.is_authenticated:
        logout_user()
        session.clear()
        flash("Logout Successful!")
        return redirect(url_for("index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for('login'))


@app.route("/create", methods=["GET", "POST"])
def create():
    """ Route for creating quizzes
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    if request.method == "POST":
        data = request.form.get("quiz_json", '')
        pprint(data)
        data = json.loads(data)

        if data['time_limit'] is None:
            data['time_limit'] = 0

        validation = Quiz.validateFields(
            title = data['title'],
            description = data['description'],
            time_limit = data['time_limit'],
            category = data['category']
        )
        if validation[0]:
            pass
        else:
            flash(validation[1])
            return render_template("create.html", title="Create", year=year, data=data)

        # i = 0
        # pprint(data["questions"])
        # print(f"length of questions list {len(data['questions'])}")
        for question in data["questions"]:
            validation = Quiz.validateQuestion(question)
            # print(f"index {i} = {question}")
            if validation[0]:
                # print(f"index {i} = {quest}")
                # quiz.addQuestion(
                #     question = quest["question"],
                #     options = quest["options"],
                #     answer = quest["answer"],
                #     score = quest["score"],
                # )
                # pprint(quiz.__dict__)
                # i += 1
                pass
            else:
                flash(validation[1])
                return render_template("create.html", title="Create", year=year, data=data)

        quiz = Quiz(
            title = data['title'],
            creator_id = current_user.get_id(),
            description = data['description'],
            time_limit = data['time_limit']
        )
        quiz.addMultipleQuestions(data['questions'])
        pprint(quiz.__dict__)
        quiz.save()
        flash("Quiz created successfully")
        return redirect(url_for('home'))

    return render_template("create.html", title="Create", year=year)


@app.route('/edit/<quiz_id>', methods=['GET', 'POST'])
def edit(quiz_id):
    """ Route for editing a users quiz if they are the creator
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))


    quiz = Quiz.get(quiz_id)
    pprint(quiz)

    if not quiz:
        flash("Invalid quiz id")
        return redirect(url_for('home'))

    if not quiz['creator_id'] == current_user.get_id():
        flash("Not authorized to edit this quiz")
        return redirect(url_for('home'))

    if request.method == "POST":
        data = request.form.get("quiz_json", '')

        session['edit_quiz_data'] = data

        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            flash("Invalid quiz data")
            return redirect(url_for('edit', quiz_id=quiz_id))

        if data['time_limit'] is None:
            data['time_limit'] = 0
        pprint(data)

        validation = Quiz.validateFields(
            title = data['title'],
            description = data['description'],
            category = data['category'],
            time_limit = data['time_limit'],
        )
        if validation[0]:
            pass
        else:
            flash(validation[1])
            return redirect(url_for('edit', quiz_id=quiz_id))

        for question in data["questions"]:
            validation = Quiz.validateQuestion(question)
            if validation[0]:
                pass
            else:
                session['edit_quiz_data'] = data
                flash(validation[1])
                return redirect(url_for('edit', quiz_id=quiz_id))

        try:
            Quiz.update(quiz_id, data)
            del session['edit_quiz_data']
            flash("Quiz updated successfully")
        except KeyError as e:
            print(e)
            flash("Quiz update failed")
        return redirect(url_for('home'))

    try:
        data = session["edit_quiz_data"]
    except KeyError:
        data = None
        pass
    url = urlparse(request.referrer) 
    if (url.netloc == '127.0.0.1:5000' or url.netloc == domain) and url.path == f'/edit/{quiz_id}' and data:
        # flash("Back in quiz bro")
        data['quiz_id'] = quiz_id
        return render_template("edit.html", title="Edit", year=year, data=data)

    return render_template("edit.html", title="Edit", year=year, data=quiz)


@app.route('/get/<quiz_id>', methods=["GET"])
def get(quiz_id):
    """ Gets a quiz and returns it as json
    """
    quiz = Quiz.get(quiz_id)
    if not quiz:
        return jsonify({
            "message": "Quiz not found"
        }), 400

    del quiz["creator_id"]
    del quiz["_id"]

    return jsonify(quiz)


@app.route('/delete/<quiz_id>', methods=['GET'])
def delete(quiz_id):
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        flash("Quiz not found")
        return redirect(request.referrer)

    if not quiz['creator_id'] == current_user.get_id():
        flash("You are not authorized to delete this quiz")
        return redirect(url_for('home'))

    try:
        Quiz.delete(quiz_id)
        flash("Quiz deleted successfully")
        return redirect(request.referrer)
    except KeyError as e:
        print(e)
        flash("Quiz deletion failed")
    return redirect(request.referrer)


@app.route('/quizinfo/<quiz_id>', methods=['GET'])
def quizinfo(quiz_id):
    """ Displays information about a quiz before it is taken
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        flash("Quiz not found")
        return redirect(request.referrer)

    return render_template('quizinfo.html', title=quiz['title'] , year=year, quiz=quiz)


@app.route('/take/<quiz_id>', methods=['GET'])
def takequiz(quiz_id):
    """ Allows user to take a quiz from.
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    quiz = Quiz.get(quiz_id)
    if quiz == None:
        flash("Quiz not found")
        return redirect(request.referrer)

    if not "taking_quiz" in session:
        start_time = datetime.now(timezone.utc)
        finish_time = start_time + timedelta(seconds=quiz["time_limit"])
        # This should cache without calling session.modified = True
        session["taking_quiz"] = {
            "quiz_id": quiz_id,
            "current_index": 0,
            "previous_index": None,
            "answers": {},
            "timeout": False,
            "finished": False,
            "start_time": start_time,
            "current_time": start_time,
            "finish_time": finish_time,
            "duration": finish_time - start_time
        }
        del start_time
        del finish_time

    # Potentially Bugged or useless
    if session["taking_quiz"]["quiz_id"] != quiz_id:
        flash("Use interface to take the quiz")
        del session["taking_quiz"]
        return redirect(url_for('home'))

    # Consider changing to redis for session storage to get faster access times by caching quiz in session

    start_time = session["taking_quiz"]["start_time"]
    session["taking_quiz"]["duration"] = session["taking_quiz"]["finish_time"] - session["taking_quiz"]["current_time"]
    session.modified = True
    return render_template(
        'takequiz.html',
        title=quiz["title"],
        year=year,
        question=quiz['questions'][session["taking_quiz"]["current_index"]],
        start_time=start_time,
        duration=int((session["taking_quiz"]["duration"]).total_seconds())
    )

@app.route('/skip/<quiz_id>', methods=["POST"])
def skip(quiz_id):
    """ Skips a quiz question
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('home'))

    session["taking_quiz"]["current_time"] = datetime.now(timezone.utc)

    quiz = Quiz.get(quiz_id)
    if quiz == None:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('home'))

    if session["taking_quiz"]["current_time"] > session["taking_quiz"]["finish_time"]:
        session["taking_quiz"]["timeout"] = True
        flash("Time Ran Out")
        return redirect(url_for('finishquiz', quiz_id=quiz_id))

    if session["taking_quiz"]["current_index"] == (len(quiz["questions"]) - 1):
        session["taking_quiz"]["finished"] = True
        return redirect(url_for('finishquiz', quiz_id=quiz_id))

    payload = request.form.get('answer')
    if not payload:
        print("No data recied when submitting quiz")
        return redirect(request.referrer)

    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        del session["taking_quiz"]
        flash("Invalid data submitted")
        return redirect(request.referrer)

    question_id, answer = list(payload['answer'].items())[0]
    del payload
    if question_id != quiz["questions"][session["taking_quiz"]["current_index"]]["question_id"]:
        del session["taking_quiz"]
        flash("Tampering detected")
        return redirect(url_for('home'))

    # answer = uuid4()
    answer = None
    session["taking_quiz"]["answers"][question_id] = {
        "question_id": question_id,
        "answer": answer
    }

    session["taking_quiz"]["previous_index"] = session["taking_quiz"]["current_index"]
    session["taking_quiz"]["current_index"] += 1 
    session.modified = True

    return redirect(url_for('takequiz', quiz_id=quiz_id))


@app.route('/previous/<quiz_id>', methods=['POST'])
def previous(quiz_id):
    """ Handles going back ward in quiz
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('home'))

    session["taking_quiz"]["current_time"] = datetime.now(timezone.utc)

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('home'))

    if session["taking_quiz"]["current_time"] > session["taking_quiz"]["finish_time"]:
        session["taking_quiz"]["timeout"] = True
        flash("Time Ran Out")
        return redirect(url_for('finishquiz', quiz_id=quiz_id))

    payload = request.form.get('answer')
    if not payload:
        print("No data recied when submitting quiz")
        return redirect(request.referrer)

    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        del session["taking_quiz"]
        flash("Invalid data submitted")
        return redirect(request.referrer)

    question_id, answer = list(payload['answer'].items())[0]
    del payload
    del answer
    if question_id != quiz["questions"][session["taking_quiz"]["current_index"]]["question_id"]:
        del session["taking_quiz"]
        flash("Tampering detected")
        return redirect(url_for('home'))

    # Store answer
    if session["taking_quiz"]["current_index"] == 0:
        flash("No previous question to do back to")
        return redirect(url_for('takequiz', quiz_id=quiz_id))

    session["taking_quiz"]["previous_index"] = session["taking_quiz"]["current_index"] - 1
    session["taking_quiz"]["current_index"] = session["taking_quiz"]["previous_index"]
    session.modified = True
    return redirect(url_for('takequiz', quiz_id=quiz_id))

@app.route('/submitanswer/<quiz_id>', methods=["POST"])
def submitanswer(quiz_id):
    """ Handles Submittion of question answers
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('home'))

    session["taking_quiz"]["current_time"] = datetime.now(timezone.utc)

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('home'))

    if session["taking_quiz"]["current_time"] > session["taking_quiz"]["finish_time"]:
        session["taking_quiz"]["timeout"] = True
        flash("Time Ran Out")
        return redirect(url_for('finishquiz', quiz_id=quiz_id))

    # if session["taking_quiz"]["current_index"] == 0 and session["taking_quiz"]["previous_index"] != None:
    #     flash("Quiz was temtered with")
    #     del session["taking_quiz"]
    #     return redirect(url_for('home'))

    payload = request.form.get('answer')
    if not payload:
        print("No data recied when submitting quiz")
        return redirect(request.referrer)

    try:
        payload = json.loads(payload)
    except json.JSONDecodeError:
        del session["taking_quiz"]
        flash("Invalid data submitted")
        return redirect(request.referrer)

    question_id, answer = list(payload['answer'].items())[0]
    del payload
    if question_id != quiz["questions"][session["taking_quiz"]["current_index"]]["question_id"]:
        del session["taking_quiz"]
        flash("Tampering detected")
        return redirect(url_for('home'))

    # Store answer
    session["taking_quiz"]["answers"][question_id] = {
        "question_id": question_id,
        "answer": answer
    }

    if session["taking_quiz"]["current_index"] == (len(quiz["questions"]) - 1):
        session["taking_quiz"]["finished"] = True
        return redirect(url_for('finishquiz', quiz_id=quiz_id))

    session["taking_quiz"]["previous_index"] = session["taking_quiz"]["current_index"]
    session["taking_quiz"]["current_index"] += 1
    session.modified = True

    return redirect(url_for('takequiz', quiz_id=quiz_id))

@app.route('/quit/<quiz_id>', methods=['POST'])
def quit(quiz_id):
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('home'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('home'))

    if session["taking_quiz"]["quiz_id"] != quiz_id:
        print("Wrong quit url")
        return redirect(url_for(request.referrer, quiz_id=quiz_id))

    return redirect(url_for('finishquiz', quiz_id=quiz_id))


@app.route('/finishquiz/<quiz_id>')
def finishquiz(quiz_id):
    """ Finishes quiz
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    if not "taking_quiz" in session:
        flash("You are not taking a quiz")
        return redirect(url_for('home'))

    quiz = Quiz.get(quiz_id)
    if not quiz:
        del session["taking_quiz"]
        flash("Quiz not found")
        return redirect(url_for('home'))

    answers = session["taking_quiz"]["answers"]
    user_score = 0
    correct_answers = 0
    questions_attempted = 0
    questions_skiped = 0
    max_score = quiz["total_score"]
    if session["taking_quiz"]["timeout"]:
        heading = f"Quiz Timeout!"
    else:
        heading = f"Quiz Finished!"

    for question in quiz["questions"]:
        question_id = question["question_id"]
        if question_id in answers.keys():
            if answers[question_id]["answer"] != None:
                questions_attempted += 1
            else:
                questions_skiped += 1
            if question["answer"] == answers[question_id]["answer"]:
                user_score += question["score"]
                correct_answers += 1
    # try:
    #     accuracy = (correct_answers/questions_attempted) * 100
    # except ZeroDivisionError:
    #     accuracy = 0
    #     pass
    if correct_answers == 0 or questions_attempted == 0:
        accuracy = 0
    else:
        accuracy = (correct_answers/questions_attempted) * 100

    if max_score:
        percentage_score = (user_score/max_score) * 100
    else:
        percentage_score = 0

    quiz_results = {
        "title": quiz["title"],
        "percentage_score": percentage_score,
        "user_score": user_score,
        "correct_answers": correct_answers,
        "questions_attempted": questions_attempted,
        "accuracy": accuracy,
        "latest_attempt": datetime.now(timezone.utc)
    }

    if not Result.check(current_user.get_id(), quiz_id):
        result_document = Result(
            current_user.get_id(),
            quiz_id,
            **quiz_results
        )
        result_document.save()
        del result_document
    else:
        try:
            Result.update(current_user.get_id(), quiz_id, quiz_results)
            print("Update Called")
        except Exception as e:
            print(e)

    del session["taking_quiz"]

    return render_template(
        'finishquiz.html', year=year,
        title=quiz['title'],
        quiz_id=quiz["quiz_id"], 
        heading=heading, 
        percentage_score=percentage_score,
        user_score=user_score,
        correct_answers=correct_answers,
        questions_attempted=questions_attempted,
        max_score=max_score,
        accuracy=accuracy
    )


@app.route('/resultinfo/<quiz_id>', methods=["GET"])
def resultinfo(quiz_id):
    """ Renders detailed results for a given quiz
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    if not Quiz.get(quiz_id):
        flash("The quiz does not exist")
        return redirect(url_for('index'))

    if not Result.check(current_user.get_id(), quiz_id):
        flash("You have not taken a quiz on this site.")
        return redirect(url_for('index'))

    result = Result.getQuizResult(
            user_id = current_user.get_id(),
    )

    return render_template("resultinfo.html", result=result)



@app.route('/myresults', methods=["GET", "POST"])
def myresults():
    """ Results page for all quizzes taken
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('login'))

    query = request.form.get('search', '')
    if query:
        results = Result.searchMyResults(current_user.get_id(), query=query)
    else:
        results = Result.getQuizResult(current_user.get_id())
        print(results)
        results = list(results) if results else None
    
    return render_template("myresults.html", results=results, query=query)


if __name__ == "__main__":
    app.run(debug=True)
