#!/usr/bin/env python3
from pprint import pprint
from models.quiz import Quiz
from models.user import User

username = "test"
email = "foo@bar.com"
password = "password123"

question1 = "What is the Capital of Foo?"
options1 = ["Lorem", "Foobar", "Bar", "Ipsum"]
answer1 = "Bar"
score1 = 10

question2 = "What is the Capital of Bar?"
options2 = ["Lorem", "Foobar", "Bar", "Ipsum"]
answer2 = "Foo"
score2 = 10

user = User(
    username = username,
    email = email,
    password = password
)

quiz = Quiz(
    creator_id = user.returnID(),
)

quiz.addQuestion(
    question = question1,
    options = options1,
    answer = answer1,
)

pprint(quiz.questions)

quiz.addQuestion(
    question = question2,
    options = options2,
    answer = answer2,
)
#
# print("\n#############\n")
#
# pprint(quiz.questions)
#
# print("\n#############\n")
#
# pprint(quiz.save())
