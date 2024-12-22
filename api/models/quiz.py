import uuid

class Quiz():
    """ Defines the datamodel for a quiz.
    """
    
    def __init__(self, creator_id, questions=[]):
        """ Initialises the quiz datamodel
        """
        self.id = str(uuid.uuid4())
        self.creator_id = creator_id
        assert isinstance(questions, list)
        self.questions = questions

    def addQuestion(self, question, options, answer, score=0):
        """ Adds a question to a quiz
        """
        assert isinstance(options, list)
        assert isinstance(answer, str)
        if answer not in options:
            print("Answer not in options!")
        question = {
            "id": str(uuid.uuid4()),
            "quiz_id": self.id,
            "question": question,
            "options": options,
            "answer": answer, 
            "score": score,
            "index": len(self.questions)
        }
        self.questions.append(question)

    def save(self):
        """ Returns JSON form of class.
        """
        return self.__dict__
