import datetime
import random
from pymongo import MongoClient
from models.quiz import Quiz
from models.user import User
from models.result import Result

client = MongoClient()

# Name of database and collections for users, quizzes and results
db = client.quiziverse


NUMBER_OF_USERS = 6
QUIZZES_PER_USER = 50
RESULTS_PER_USER = 50

if RESULTS_PER_USER > (NUMBER_OF_USERS * QUIZZES_PER_USER):
    print("Number of results must be less than the product of NUMBER_OF_USERS and QUIZZES_PER_USER")

questions_1 = [
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
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Lyon", "Marseille", "Nice"],
        "answer": "Paris",
        "score": 10
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["Tokyo", "Osaka", "Kyoto", "Hiroshima"],
        "answer": "Tokyo",
        "score": 10
    },
    {
        "question": "What is the capital of Brazil?",
        "options": ["Brasília", "Rio de Janeiro", "São Paulo", "Salvador"],
        "answer": "Brasília",
        "score": 10
    },
]

questions_2 = [
    {
        "question": "Which country is credited with inventing pizza?",
        "options": ["Italy", "Greece", "USA", "France"],
        "answer": "Italy",
        "score": 10
    },
    {
        "question": "Where was the hamburger first made?",
        "options": ["Germany", "USA", "France", "Denmark"],
        "answer": "Germany",
        "score": 10
    },
    {
        "question": "Which country is known as the birthplace of sushi?",
        "options": ["Japan", "China", "Korea", "Thailand"],
        "answer": "Japan",
        "score": 10
    },
    {
        "question": "From which country did chocolate originate?",
        "options": ["Mexico", "Belgium", "Switzerland", "USA"],
        "answer": "Mexico",
        "score": 10
    },
    {
        "question": "Which country is the origin of croissants?",
        "options": ["France", "Austria", "Italy", "Switzerland"],
        "answer": "Austria",
        "score": 10
    },
]

questions_3 = [
    {
        "question": "Which ancient wonder was located in Egypt?",
        "options": ["Hanging Gardens of Babylon", "Statue of Zeus", "Great Pyramid of Giza", "Colossus of Rhodes"],
        "answer": "Great Pyramid of Giza",
        "score": 10
    },
    {
        "question": "Who was the first President of the United States?",
        "options": ["Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams"],
        "answer": "George Washington",
        "score": 10
    },
    {
        "question": "What year did World War II end?",
        "options": ["1943", "1945", "1947", "1950"],
        "answer": "1945",
        "score": 10
    },
    {
        "question": "Which empire was ruled by Julius Caesar?",
        "options": ["Greek Empire", "Roman Empire", "Ottoman Empire", "Persian Empire"],
        "answer": "Roman Empire",
        "score": 10
    },
    {
        "question": "What was the name of the ship that carried the Pilgrims to America in 1620?",
        "options": ["Mayflower", "Santa Maria", "Endeavour", "Beagle"],
        "answer": "Mayflower",
        "score": 10
    },
]

user_list = []

# Create Users
for i in range(1, NUMBER_OF_USERS + 1):
    user = User(
        username = f"Test_{i}",
        email = f"test_{i}@foo.bar",
        password = "q",
    )
    user_list.append(user.id)
    user.save()

print(f"Created {len(user_list)} Users")

quiz_list = []
quiz_titles = {}

for user_id in user_list[:2]:
    numb = QUIZZES_PER_USER
    for number in range (1, numb + 1):
        title = f"The Capital cities of the world {random.randrange(1000)}"
        quiz = Quiz(
            title = title,
            description = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Hic ut voluptate temporibus aliquam nihil tenetur quibusdam ipsam optio odio ex.",
            creator_id = user_id,
            time_limit = 600
        )
        quiz.addMultipleQuestions(questions_1)
        quiz_list.append(quiz.quiz_id)
        quiz_titles[quiz.quiz_id] = quiz.title

for user_id in user_list[2:4]:
    numb = QUIZZES_PER_USER
    for number in range (1, numb + 1):
        title = f"The origins of food {random.randrange(1000)}"
        quiz = Quiz(
            title = title,
            description = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Hic ut voluptate temporibus aliquam nihil tenetur quibusdam ipsam optio odio ex.",
            creator_id = user_id,
            time_limit = 600
        )
        quiz.addMultipleQuestions(questions_2)
        quiz_list.append(quiz.quiz_id)
        quiz_titles[quiz.quiz_id] = quiz.title

for user_id in user_list[4:]:
    numb = QUIZZES_PER_USER
    for number in range (1, numb + 1):
        title = f"Randon fun facts {random.randrange(1000)}"
        quiz = Quiz(
            title = title,
            description = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Hic ut voluptate temporibus aliquam nihil tenetur quibusdam ipsam optio odio ex.",
            creator_id = user_id,
            time_limit = 600
        )
        quiz.addMultipleQuestions(questions_2)
        quiz.save()
        quiz_list.append(quiz.quiz_id)
        quiz_titles[quiz.quiz_id] = quiz.title

print(f"Created {len(quiz_list)} Quizzes")

results = []
for user_id in user_list:
    for result in range(RESULTS_PER_USER):
        quiz_id = random.choice(quiz_list)
        result = Result(
            user_id = user_id,
            quiz_id = quiz_id,
            title = quiz_titles[quiz_id],
            percentage_score = 100,
            user_score = 5,
            correct_answers = 5,
            questions_attempted = 5,
            accuracy = 100,
            latest_attempt = datetime.datetime.now(datetime.timezone.utc)
        )
        result.save()
        results.append(result)

print(f"Created {len(results)} Results")
