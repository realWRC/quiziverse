#!/usr/bin/env python3
from pprint import pprint
from models.quiz import Quiz
from models.user import User

title = "Capital Cities Quiz"

username = "test"
email = "foo@bar.com"
password = "password123"

question1 = "What is the Capital of Foo?"
options1 = ["Lorem", "Foobar", "Bar", "Ipsum"]
answer1 = "Bar"
score1 = 10

question2 = "What is the Capital of Bar?"
options2 = ["Lorem", "Foobar", "Bar", "Ipsum"]
answer2 = "Ipsum"
score2 = 10

questions = [
    {
        "question": question1,
        "options": options1,
        "answer": answer1,
        "score": score1
    },
    {
        "question": question2,
        "options": options2,
        "answer": answer2,
        "score": score2
    },
]

user = User(
    username = username,
    email = email,
    password = password
)

quiz = Quiz(
    title = title,
    creator_id = user.returnID(),
    questions = questions
)

pprint(quiz.save())

print("\n########\n")


quiz.addQuestion(
    question = question1,
    options = options1,
    answer = answer1,
)
quiz.addQuestion(
    question = question2,
    options = options2,
    answer = answer2,
)

pprint(quiz.save())

print("\n########\n")
