import uuid
from models import db
from datetime import datetime, timezone

class Quiz():
    """ Defines the datamodel for a quiz.
    """
    
    def __init__(self, title, creator_id, description, category="general", quiz_id=str(uuid.uuid4()), questions=[], time_limit=0, total_score=0, **kwargs):
        """ Initialises the quiz datamodel
        """
        validation = Quiz.validateFields(title, description, category, time_limit)
        if isinstance(questions, list) and validation[0]:
            self.quiz_id = quiz_id
            self.title = title
            self.creator_id = creator_id
            self.description = str(description).strip()
            self.category = category
            self.time_limit = time_limit
            self.total_score = total_score
            self.questions = questions
            self.creatated_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)
        else:
            return validation[1]

    def addMultipleQuestions(self, questions):
        """ Adds a list of questions to the quiz at once
        """
        original_questions = self.questions
        original_total_score = self.total_score
        final_score = 0
        if questions:
            questionSet = []
            # keys = ['question', 'options', 'answer', 'score'] 
            for question in questions:
                # if isinstance(question, dict) and  all(key in question for key in keys):
                validation = Quiz.validateQuestion(question)
                if validation[0]:
                    final_score += self.__addMultipleQuestionsHelper(
                        questionSet = questionSet,
                        question = question['question'],
                        options = question['options'],
                        answer = question['answer'],
                        score = question['score']
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
        """ Adds a question to a quiz
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
                "question": question,
                "options": options,
                "answer": answer, 
                "score": score,
                "index": len(self.questions)
            }
            self.questions.append(question)
            self.total_score += score
            self.updated_at = datetime.now(timezone.utc)
        else:
            print(validation[1])

    def __addMultipleQuestionsHelper(self, questionSet, question, options, answer, score=1):
        """ Adds a question to a quiz
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
        """ Returns JSON form of class.
        """
        return db.quizzes.insert_one(self.__dict__)

    @staticmethod
    def recreate(quiz_id):
        """ Recreates quiz by id
        """
        quiz_dict = Quiz.get(quiz_id)
        if quiz_dict:
            quiz = Quiz(
                title = quiz_dict["title"],
                quiz_id = quiz_dict["quiz_id"],
                creator_id = quiz_dict["creator_id"],
                description = quiz_dict["description"],
                category = quiz_dict["category"],
                time_limit = quiz_dict["time_limit"],
                total_score = quiz_dict["total_score"],
                creatated_at = quiz_dict["creatated_at"],
                updated_at = quiz_dict["updated_at"],
                questions = quiz_dict["questions"]
            )
            return quiz

    @staticmethod
    def validateQuestion(question):
        """ Validates the content of a question dict for the class
        Quiz
        """ 
        keys = ['question', 'options', 'answer', 'score'] 
        if isinstance(question, dict):
            if not all(key in question for key in keys):
                return (False, "A key is missing from the question dictionary.")
            if not isinstance(question['options'], list):
                return (False, "Options must be an array or list of strings.")
            if len(question["options"]) > 4:
                return (False, "A question cannot have more that 4 options")

            # Strip of all empty spaces if strings
            if isinstance(question["question"], str):
                question["question"].strip()

            for option in question["options"]:
                if isinstance(option, str):
                    option.strip()
            if isinstance(question["answer"], str):
                question["answer"].strip()

            if not question['answer'] in question['options']:
                return (False, "The answer must match one of the questions.")
            if not isinstance(question['score'], int) and not isinstance(question['score'], float):
                return (False, "The score must be a number")
            return (True, "Valid")
        else:
            return (False, "Questions must be a dict.")

    @staticmethod
    def validateFields(title, description, category, time_limit):
        """ Validates all external direct attributes of a Quiz object except creator_id
        and questions.
        """
        if not isinstance(title, str) or title.isnumeric():
            return (False, "Title must be a string")
        if not isinstance(description, str):
            return (False, "Use words to fill the description")
        if not isinstance(category, str):
            return (False, "Category must be a string")
        if not isinstance(time_limit, int) and not isinstance(time_limit, float):
            return (False, "Time Limit must be an Integer or a Float")

        title.strip()
        description.strip()
        category.strip()

        return (True, "Valid fields")

    @staticmethod
    def get(quiz_id):
        """ Returns a quiz by ID from the database
        """
        return db.quizzes.find_one({"quiz_id": quiz_id})

    @staticmethod
    def getAll():
        """ Gets all quizzes from database and orders them by title and date updated_at
        """
        return db.quizzes.find().sort([("title", 1), ("updated_at", 1)])

    @staticmethod
    def getByFilter(criteria):
        """ Returns quiz by a given field
        """
        return db.quizzes.find(criteria)

    @staticmethod
    def delete(quiz_id):
        """ Deletes quiz by id
        """
        result = db.quizzes.delete_one({"quiz_id": quiz_id})
        if result.acknowledged and result.deleted_count == 1:
            pass
        else:
            raise KeyError("Quiz delete operation failed")

    @staticmethod
    def check(quiz_id):
        """ Checks if a quiz_id is valid
        """
        if db.results.find_one({"user_id": quiz_id}, {"_id": 1}):
            return True
        else:
            return False

    @staticmethod
    def update(quiz_id, data):
        """ Updates a quiz object from storage
        """
        temp = Quiz.recreate(quiz_id)
        assert temp is not None
        temp.addMultipleQuestions(data["questions"])

        result = db.quizzes.update_one(
            {"quiz_id": quiz_id },
            { "$set": {
                "title": data['title'],
                "questions": temp.questions,
                "total_score": temp.total_score,
                "time_limit": data['time_limit'],
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        del temp
        if result.modified_count == 0:
            raise KeyError("Pymongo could not update the document due to an invalid quiz_id")

    @staticmethod
    def search(query):
        """ Searches quiz database
        """
        result = db.quizzes.find(
            {"title": {"$regex": query, "$options": "i"}}
            ).sort([("title", 1), ("updated_at", 1)])

        test = result.__copy__()
        if len(list(test)):
            del test
            print("IN SEARCH RESULT FOUND")
            return result
        else:
            return None
