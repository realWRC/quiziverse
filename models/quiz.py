import uuid
from models import db

class Quiz():
    """ Defines the datamodel for a quiz.
    """
    
    def __init__(self, title, creator_id, quiz_id=str(uuid.uuid4()), questions=[], time_limit=0, total_score=0):
        """ Initialises the quiz datamodel
        """
        if isinstance(questions, list):
            self.quiz_id = quiz_id
            self.title = title
            self.creator_id = creator_id
            self.time_limit = time_limit
            self.total_score = total_score
            self.questions = questions

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
                "question": question,
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
                time_limit = quiz_dict["time_limit"],
                total_score = quiz_dict["total_score"],
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
            if not question['answer'] in question['options']:
                return (False, "The answer must match one of the questions.")
            if not isinstance(question['score'], int) and not isinstance(question['score'], float):
                return (False, "The score must be a number")
            return (True, "Valid")
        else:
            return (False, "Questions must be a dict.")

    @staticmethod
    def validateFields(title, time_limit):
        """ Validates all external direct attributes of a Quiz object except creator_id
        and questions.
        """
        if not isinstance(title, str):
            return (False, "Title must be a string")
        if not isinstance(time_limit, int) and not isinstance(time_limit, float):
            return (False, "Time Limit must be an Integer or a Float")
        return (True, "Valid fields")

    @staticmethod
    def get(quiz_id):
        """ Returns a quiz by ID from the database
        """
        return db.quizzes.find_one({"quiz_id": quiz_id})

    @staticmethod
    def getAll():
        """ Gets all quizzes from database
        """
        return db.quizzes.find()

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
    def update(quiz_id, data):
        """ Updates a quiz object from storage
        """
        # temp = Quiz(
        #     title = data["title"],
        #     creator_id = "dummy id",
        #     time_limit = data["time_limit"],
        # )
        # temp.addMultipleQuestions(data["questions"])
        temp = Quiz.recreate(quiz_id)
        assert temp is not None
        temp.addMultipleQuestions(data["questions"])

        result = db.quizzes.update_one(
            {"quiz_id": quiz_id },
            { "$set": {
                "title": temp.title,
                "questions": temp.questions,
                "total_score": temp.total_score,
                "time_limit": temp.time_limit,
            }}
        )
        del temp
        if result.modified_count == 0:
            raise KeyError("Pymongo could not update the document due to an invalid quiz_id")
