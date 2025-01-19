from models import resultsCollection

class Result():
    """
    Object model for how results will be stored.

    Attributes:
        user_id(str): Unique identifier of a user.
        quiz_id(str): Unique identifier of a quiz.
        title(str): The title of a quiz.
        user_score(int/float):The score of the user on that quiz
        percentage_score(int/float): The score of the result as a
        percentage.
        correct_answers(int): Number of questions answered correctly.
        accuracy(float): The number of correct answers as a percentage
        of the number of questions.
        latest_attempt(str): Time aware(utc) datetime string
    """

    def __init__(self, user_id, quiz_id, **kwargs):
        """
        Initialises a result object.

        Args:
            user_id(str): Unique identifier of a user.
            quiz_id(str): Unique identifier of a quiz.
            kwargs(dict): An arbitrary dictionary containing infromation
            to initialise result attributes.
        """
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
        """
        Saves the results object as a dictionary using the __dict__
        method.

        Returns:
            InsertOneReult: Pymongo class with information about the
            insertion operation
        """
        return resultsCollection.insert_one(self.__dict__)

    @staticmethod
    def check(user_id, quiz_id):
        """
        Checks if user with user_id has a results document that has
        a given quiz_id return true if it does.

        Args:
            user_id(str): Unique identifier of a user.
            quiz_id(str): Unique identifier of a quiz.

        Returns:
            bool: True is the user has a result with given quiz_id
            or else false.
        """
        return resultsCollection.find_one(
            {"user_id": user_id, "quiz_id": quiz_id}, {"_id": 1}
        ) is not None

    @staticmethod
    def getQuizResult(user_id):
        """
        Retrieves all results for a user in the results collection.

        Args:
            user_id(str): Unique identifier of a user.
        Return:
            list: A list of dictionaries representing the results.
            None: If no results were found.
        """
        match = resultsCollection.find({"user_id": user_id})
        if match:
            return list(match)
        else:
            return None

    # TODO This function was useful for a previous data model and
    # is no longer userful. It should be removed
    @staticmethod
    def getByUserID(user_id):
        """
        Retrieves a results object for a user in the results collection.

        Args:
            user_id(str): Unique identifier of a user.
        Return:
            dict: The data of a results object.
            None: If no results were found.
        """
        return resultsCollection.find_one({"user_id": user_id})

    # TODO Execute check method before using this
    @staticmethod
    def delete(user_id, quiz_id):
        """
        Deletes data for a result from the database

        Args:
            user_id(str): Unique identifier of a user.
            quiz_id(str): Unique identifier of a quiz.
        """
        resultsCollection.delete_one({"user_id": user_id, "quiz_id": quiz_id})

    @staticmethod
    def update(user_id, quiz_id, kwargs):
        resultsCollection.update_one(
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
        """ 
        Collects all results by user_id and searched for titles
        that match the given query.

        Args:
            user_id(str): Unique user identifier.
            query(str): The title to be searched for
        Returns:
            list: A list of results that match the query.
            None: If no results that match the query are found.
        """
        cursor = resultsCollection.find(
            {
                "user_id": user_id,
                "title": {"$regex": query, "$options": "i"}
            }
        ).sort([("title", 1), ("latest_attempt", 1)])

        results = list(cursor)
        if results:
            return results
        else:
            return None
