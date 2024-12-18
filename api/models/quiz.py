import uuid
from models import db

class Quiz():
    """ Defines the datamodel for a quiz.
    """
    
    def __init__(self, creator_id, questions=[]):
        """ Initialises the quiz datamodel
        """
        self.id = uuid.uuid4()
        self.creator = creator_id
        assert isinstance(questions, list)
        self.questions = questions

    def addQuestion(self, question, options, answer, score=0):
        """ Adds a question to a quiz
        """
        assert isinstance(options, list)
        assert answer in options
        question = {
            "id": str(uuid.uuid4()),
            "quiz_id": self.id,
            "question": question,
            "options": options,
            "answer": answer, 
            "score": score
        }
        self.questions.append(question)
