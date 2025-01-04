from pymongo import MongoClient
from models.quiz import Quiz
from models.user import User

client = MongoClient()
db = client.quiziverse

questions = [
    {
        "question": "What is the capital of Malawi?",
        "options": ["Lilongwe", "Mzuzu", "Karonga", "Blantyre"],
        "answer": "Lilongwe",
        "score": 10
    },
    {
        "question": "What is the capital of the USA?",
        "options": ["Washington", "New York", "New Jersey", "California"],
        "answer": "Washington",
        "score": 10
    },
]

user = User.getByUsername("Test")
assert user is not None

numb = 100
user_id = user.id

for number in range (1, numb + 1):
    title = f"Capital Cities {number}"
    quiz = Quiz(
        title = title,
        creator_id = user_id,
        time_limit = 600
    )
    quiz.addMultipleQuestions(questions)
    quiz.save()
