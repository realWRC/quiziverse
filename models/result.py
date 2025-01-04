from uuid import uuid4
from models import db


class Result():
    """ Object model for how results will be stored.
    """

    def __init__(self, user_id, results=[]):
        self.result_id = str(uuid4)
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
        if db.results.find_one({"user_id": user_id}, {"_id": 1}):
            return True
        else:
            return False

    @staticmethod
    def getByUserID(user_id):
        return db.results.find_one({"user_id": user_id})

    @staticmethod
    def update(user_id, quiz_id, results):
        results["quiz_id"] = quiz_id

        query = db.results.update_one(
                {"user_id": user_id},
                { "$push": {
                    "results": {
                        "$each": [results],
                        "$position": 0
                        }
                    }}
        )
        if query.matched_count != 1 or query.modified_count != 1:
            raise Exception("User does not have results collection")
