from uuid import uuid4
from models import db
from pymongo.errors import PyMongoError


class Result():
    """ Object model for how results will be stored.
    """

    def __init__(self, user_id, quiz_id, **kwargs):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.title = kwargs["title"]
        self.percentage_score = kwargs["percentage_score"]
        self.user_score = kwargs["user_score"]
        self.correct_answers = kwargs["correct_answers"]
        self.questions_attempted = kwargs["correct_answers"]
        self.accuracy = kwargs["accuracy"]
        self.latest_attempt = kwargs["latest_attempt"]

    def save(self):
        """ Saves the results object
        """
        return db.results.insert_one(self.__dict__)

    @staticmethod
    def check(user_id, quiz_id):
        """ Checks if user with user_id has a results document
        return true if it does
        """
        return db.results.find_one({"user_id": user_id, "quiz_id": quiz_id}, {"_id": 1}) is not None

    @staticmethod
    def getQuizResult(user_id):
        """ Retrieves results for a user in results collection
        """
        match = db.results.find({"user_id": user_id})
        if match:
            return match
        else:
            return None

    @staticmethod
    def getByUserID(user_id):
        return db.results.find_one({"user_id": user_id})

    @staticmethod
    def delete(user_id, quiz_id):
        db.results.delete_one({"user_id": user_id, "quiz_id": quiz_id})

    @staticmethod
    def update(user_id, quiz_id, kwargs):
        db.results.update_one(
            {"user_id": user_id, "quiz_id": quiz_id},
            {"$set": {
                "title": kwargs["title"],
                "percentage_score": kwargs["percentage_score"],
                "user_score": kwargs["user_score"],
                "correct_answers": kwargs["correct_answers"],
                "questions_attempted": kwargs["correct_answers"],
                "accuracy": kwargs["accuracy"],
                "latest_attempt": kwargs["latest_attempt"]
                }}
        )
        
    @staticmethod
    def searchMyResults(user_id, query):
        """ Collects all results by user_id and query them based on title.
        """
        cursor = db.results.find(
            {
                "user_id": user_id,
                "title": {"$regex": query, "$options": "i"}
            }
        ).sort([("title", 1), ("latest_attempt", 1)])

        # test = result.__copy__()
        # if len(list(result)):
        #     del test
        #     return result
        # else:
        #     return None
        results = list(cursor)
        
        if results:
            return results
        else:
            return None
