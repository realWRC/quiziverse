import uuid
from models import quizzesCollection, resultsCollection
from datetime import datetime, timezone


class Quiz():
    """
    Defines the datamodel/datastructure for a quiz.

    Args:
        title(str): The title of the quiz.
        creator_id(str): The user id of the the quizzes creator.
        description(str): A short 300 character description of the quiz.
        category(str): The group to which a quiz can be grouped into.
        quiz_id(str): The unique identifier for a quiz.
        questions(list): A list of dictionaries which represent a question.
        time_limit(int): The time to finish a quiz in seconds.
        total_score(int): The sum of the scores of all questions.
        kwargs(dict): An arbitrary dictionary to add new fields.
    """

    def __init__(
            self, title, creator_id, description, category="general",
            quiz_id=None, questions=None, time_limit=0, total_score=0,
            **kwargs):
        """ 
        Initialises an instance of a Quiz class. Performs validation using
        the validateFields staticmethod defined below.

        Args:
            title(str): The title of the quiz.
            creator_id(str): The user id of the the quizzes creator.
            description(str): A short 300 character description of the quiz.
            category(str): The group to which a quiz can be grouped into.
            quiz_id(str): The unique identifier for a quiz.
            questions(list): A list of dictionaries where each dict
            represents a question.
            time_limit(int): The time to finish a quiz in seconds.
            total_score(int/float): The sum of the scores of all questions.
            kwargs(dict): An arbitrary dictionary to add new fields.
        """
        if quiz_id is None:
            quiz_id = str(uuid.uuid4())
        if questions is None:
            questions = []
        validation = Quiz.validateFields(
                title, description, category, time_limit
                )
        if isinstance(questions, list) and validation[0]:
            self.quiz_id = quiz_id
            self.title = title
            self.creator_id = creator_id
            self.description = str(description).strip()
            self.category = category
            self.time_limit = time_limit
            self.total_score = total_score
            self.questions = questions
            self.created_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)
        else:
            return validation[1]

    def addMultipleQuestions(self, questions):
        """ 
        Adds a list of questions to a quiz instance at once. It will copy
        the original question set, attempt to create a new question set and
        assign it to the Quiz instance if it success. Every question in the
        list is validated using the validateQuestion staticmethod defined
        below.

        Args:
            questions(list): A list of dictionaries, each representing
            a question.

        Returns:
            list: A list of dictionaries that is assigned to the quiz
            on success or an empty list if validation failed.
        """
        original_questions = self.questions
        original_total_score = self.total_score
        final_score = 0
        if questions:
            questionSet = []
            for question in questions:
                validation = Quiz.validateQuestion(question)
                if validation[0]:
                    final_score += self.__addMultipleQuestionsHelper(
                        questionSet=questionSet,
                        question=question['question'],
                        options=question['options'],
                        answer=question['answer'],
                        score=question['score']
                    )
                else:
                    self.questions = original_questions
                    self.total_score = original_total_score
                    print(validation[1])
            self.questions = questionSet
            self.total_score = final_score
            self.updated_at = datetime.now(timezone.utc)
            return questionSet
        else:
            return []

    def addQuestion(self, question, options, answer, score=1):
        """
        adds a question to a quiz object instance. validates the
        question using validatequestion staticmethod.

        args:
            question(str): the question being asked.
            options(list): a list representing the possible answers
            to the question.
            answers(str): a string representing the answer.
            score(int/float): the score of a question 1 by default.
        """
        validation = Quiz.validateQuestion({
            "question": question,
            "options": options,
            "answer": answer,
            "score": score,
        })
        if validation[0]:
            validated_question = {
                "question_id": str(uuid.uuid4()),
                "quiz_id": self.quiz_id,
                "question": question,
                "options": options,
                "answer": answer,
                "score": score,
                "index": len(self.questions)
            }
            self.questions.append(validated_question)
            self.total_score += score
            self.updated_at = datetime.now(timezone.utc)
        else:
            print(validation[1])

    def __addMultipleQuestionsHelper(
            self, questionSet, question,
            options, answer, score=1):
        """ 
        Adds a question to a given list object. validates the
        question using validatequestion staticmethod.

        args:
            questionSet(list): A list to which a validated question is
            appended
            question(str): The question being asked.
            options(list): A list representing the possible answers
            to the question.
            answers(str): A string representing the answer.
            score(int/float): The score of a question 1 by default.
        
        Returns:
            int: The score of the question added.

        Raises:
            TypeError: If validation fails raise TypeError with the
            message on the validation that failed.
        """
        validation = Quiz.validateQuestion({
            "question": question,
            "options": options,
            "answer": answer,
            "score": score,
        })
        if validation[0]:
            question = {
                "question_id": str(uuid.uuid4()),
                "quiz_id": self.quiz_id,
                "question": question.strip(),
                "options": options,
                "answer": answer,
                "score": score,
                "index": len(questionSet)
            }
            questionSet.append(question)
            return score
        else:
            raise TypeError(validation[1])

    def save(self):
        """
        Saves am instace of a Quiz object to the database as
        a dictionary using the default __dict__ method.
        """
        return quizzesCollection.insert_one(self.__dict__)

    @staticmethod
    def recreate(quiz_id):
        """ 
        Recreates Quiz object instace based on its quiz_id.

        Args:
            quiz_id(str): A unique identifier for a quiz.

        Returns:
            Quiz: A quiz object corresponding to the quiz_id.
            None: If not quiz matches the given quiz_id.
        """
        quiz_dict = Quiz.get(quiz_id)
        if quiz_dict:
            quiz = Quiz(
                title=quiz_dict["title"],
                quiz_id=quiz_dict["quiz_id"],
                creator_id=quiz_dict["creator_id"],
                description=quiz_dict["description"],
                category=quiz_dict["category"],
                time_limit=quiz_dict["time_limit"],
                total_score=quiz_dict["total_score"],
                creatated_at=quiz_dict["created_at"],
                updated_at=quiz_dict["updated_at"],
                questions=quiz_dict["questions"]
            )
            return quiz

    @staticmethod
    def validateQuestion(question):
        """
        Validates the content of a question dict to be assigned to Quiz
        instance questions attribute.

        Args:
            question(dict): A dictionary represting a question.

        Return:
            Tuple: A tuple with a bool and a string message.
        """
        keys = ['question', 'options', 'answer', 'score']
        if isinstance(question, dict):
            if not all(key in question for key in keys):
                return (
                    False, "A key is missing from the question dictionary."
                )
            if not isinstance(question['options'], list):
                return (
                    False, "Options must be an array or list of strings."
                )
            if len(question["options"]) > 4:
                return (
                    False, "A question cannot have more that 4 options"
                )

            # Strip of all empty spaces if strings
            if isinstance(question["question"], str):
                question["question"].strip()

            for option in question["options"]:
                if isinstance(option, str):
                    option.strip()
            if isinstance(question["answer"], str):
                question["answer"].strip()

            if not question['answer'] in question['options']:
                return (
                    False, "The answer must match one of the questions."
                )
            if not isinstance(question['score'], int) and not\
                    isinstance(question['score'], float):
                return (False, "The score must be a number")
            return (True, "Valid")
        else:
            return (False, "Questions must be a dict.")

    @staticmethod
    def validateFields(title, description, category, time_limit):
        """
        Validates attributes of a Quiz object prior to assignment
        except creator_id and questions.

        Args:
            title(str): The title of the quiz
            description(str): A short 300 character description of the quiz.
            category(str): The group to which a quiz can be grouped into.
            time_limit(int): The time to finish a quiz in seconds.

        Return:
            Tuple: A tuple with a bool and a string message.
        """
        if not isinstance(title, str) or title.isnumeric():
            return (False, "Title must be a string")
        if not isinstance(description, str):
            return (False, "Use words to fill the description")
        if not isinstance(category, str):
            return (False, "Category must be a string")
        if not isinstance(time_limit, int) and \
                not isinstance(time_limit, float):
            return (False, "Time Limit must be an Integer or a Float")
        title.strip()
        description.strip()
        category.strip()
        return (True, "Valid fields")

    @staticmethod
    def get(quiz_id):
        """
        Retrieves data for a quiz that corresponds to the qiven quiz_id
        from the database.

        Args:
            quiz_id(str): A unique identifier for a quiz.

        Return:
            cursor: Iterable pymongo cursor object with the quiz data.
            None: If the quiz with the given id is not found.
        """
        return quizzesCollection.find_one({"quiz_id": quiz_id})

    @staticmethod
    def getAll():
        """
        Retrieves all quizzes from database and orders them by title and date
        updated_at.

        Return:
            cursor: Iterable pymongo cursor object with the quiz data.
            None: If the quiz with the given id is not found.
        """
        return quizzesCollection.find().sort([("title", 1), ("updated_at", 1)])

    @staticmethod
    def getAllUserQuizzes(creator_id):
        """
        Gets all quizzes created by a user with a given creator_id.

        Args:
            creator_id(str): A unique identifier for a user(user id).

        Return:
            cursor: Iterable pymongo cursor object with the quiz data.
            None: If the quiz with the given id is not found.
        """
        return quizzesCollection.find({"creator_id": creator_id})

    @staticmethod
    def getByFilter(criteria):
        """
        Searches the quiz collection using given criteria.

        Args:
            criteria(dict): A dict using pymongo seach syntax for the find
            function.

        Returns:
            cursor: Iterable pymongo cursor object with the quiz data.
            None: If the quiz with the given id is not found.
        """
        return quizzesCollection.find(criteria)

    # TODO refactor to clarify if database failed or quiz was not found
    # check staticmethod can help with this
    @staticmethod
    def delete(quiz_id):
        """
        Deletes quiz data from the database using a given quiz_id.

        Args:
            quiz_id(str): A unique identifier for a quiz.

        Raises:
            KeyError: When the delete operation fails of any reason.
        """
        result = quizzesCollection.delete_one({"quiz_id": quiz_id})
        if result.acknowledged and result.deleted_count == 1:
            pass
        else:
            raise KeyError("Quiz delete operation failed")

    @staticmethod
    def check(quiz_id):
        """ 
        Checks if a quiz with a given quiz_id exists in the database.

        Args:
            quiz_id(str): A unique identifier for a quiz.

        Returns:
            bool: True if it is in the database and false otherwise.
        """
        if resultsCollection.find_one({"user_id": quiz_id}, {"_id": 1}):
            return True
        else:
            return False

    @staticmethod
    def update(quiz_id, data):
        """
        Updates the data of a quiz with a given quiz_id in storage.

        Args:
            quiz_id(str): A unique identifier for a quiz.
            data(dict): A dict containing new data to update the quiz.
        """
        temp = Quiz.recreate(quiz_id)
        assert temp is not None
        temp.addMultipleQuestions(data["questions"])

        result = quizzesCollection.update_one(
            {
                "quiz_id": quiz_id
            },
            {
                "$set":
                {
                    "title": data['title'],
                    "questions": temp.questions,
                    "total_score": temp.total_score,
                    "time_limit": data['time_limit'],
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        del temp
        if result.modified_count == 0:
            raise KeyError(
                "Pymongo could not update the document \
                        due to an invalid quiz_id"
            )

    @staticmethod
    def search(query):
        """ 
        Searches the quiz database(collection) for a quiz
        whose title matches the query.

        Args:
            query(str): A title to be searched for.

        Returns:
            list: A list containing the data of all quizzes that
            match the query.
            None: No quiz in the database does not match the query.
        """
        result = quizzesCollection.find(
            {"title": {"$regex": query, "$options": "i"}}
            ).sort([("title", 1), ("updated_at", 1)])

        test = result.__copy__()
        if len(list(test)):
            del test
            print("IN SEARCH RESULT FOUND")
            return result
        else:
            return None

    @staticmethod
    def searchUserQuizzes(creator_id, query):
        """
        Searches all quizzes made by user with creator_id and
        searches for a quiz whose title matches the given
        query.

        Args:
            creator_id(str): Unique identifier of the quizzes creator.
            query(str): A title to be searched for.

        Returns:
            list: A list containing the data of all quizzes that
            match the query.
            None: No quiz in the database does not match the query.
        """
        cursor = quizzesCollection.find(
            {
                "creator_id": creator_id,
                "title": {"$regex": query, "$options": "i"}
            }
        ).sort([("title", 1), ("updated_at", 1)])

        result = list(cursor)
        if result:
            return result
        else:
            return None
