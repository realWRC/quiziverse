from pymongo import MongoClient

client = MongoClient()
db = client.quiziverse

quizzesCollection = db.quizzes
usersCollection = db.users
resultsCollection = db.results
