from uuid import uuid4
from models import db
from pymongo.errors import PyMongoError


class Result():
    """ Object model for how results will be stored.
    """

    def __init__(self, user_id, results=[]):
        self.result_id = str(uuid4())
        self.user_id = user_id
        self.results = results

    def save(self):
        """ Saves the results object
        """
        return db.results.insert_one(self.__dict__)

    @staticmethod
    def check(user_id):
        """ Checks if user with user_id has a results document
        return true if it does
        """
        return db.results.find_one({"user_id": user_id}, {"_id": 1}) is not None

    @staticmethod
    def getQuizResult(user_id, quiz_id):
        """ Retrieves results for a quiz in user results collection
        """
        pipeline = [
            {
                "$match": {
                    "user_id": user_id, 
                }
            },
            { "$project": {
                "_id": 0,
                "match": {
                    "$filter": {
                        "input": "$results",
                        "as": "result",
                        "cond": {"$eq": ["$$result.quiz_id", quiz_id]}
                        }
                    }
                }
            }
        ]
        match = list(db.results.aggregate(pipeline))
        if match and match[0]["match"]:
            return match[0]["match"][0]
        else:
            return None

    @staticmethod
    def getByUserID(user_id):
        return db.results.find_one({"user_id": user_id})

    @staticmethod
    def update(user_id, quiz_id, results):
        
        db.results.update_one(
            {"user_id": user_id},
            {"$pull": {
                "results": {
                    "quiz_id": quiz_id,
                    }
            }}
        )

        db.results.update_one(
            {"user_id": user_id},
            { "$push": {
                "results": {
                    "$each": [results],
                    "$position": 0
                    }
                }}
        )
