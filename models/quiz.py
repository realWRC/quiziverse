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
                if Quiz.validateQuestion(question):
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
                    raise TypeError("Question has wrong value")
            self.questions = questionSet
            self.total_score = final_score
            return questionSet
        else:
            return []

    def addQuestion(self, question, options, answer, score=1):
        """ Adds a question to a quiz
        """
        assert isinstance(options, list)
        assert isinstance(answer, str)
        if answer not in options:
            print("Answer not in options!")
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

    def __addMultipleQuestionsHelper(self, questionSet, question, options, answer, score=1):
        """ Adds a question to a quiz
        """
        assert isinstance(questionSet, list)
        assert isinstance(options, list)
        assert isinstance(answer, str)
        if answer not in options:
            print("Answer not in options!")
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
        if isinstance(question, dict) and  all(key in question for key in keys):
            return True
        else:
            return False

    @staticmethod
    def get(quiz_id):
        """ Returns a quiz by ID from the database
        """
        return db.quizzes.find_one({"quiz_id": quiz_id})

    @staticmethod
    def delete(quiz_id):
        """ Deletes quiz by id
        """
        return db.quizzes.delete_one({"quiz_id": quiz_id})
