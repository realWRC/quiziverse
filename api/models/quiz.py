import uuid

class Quiz():
    """ Defines the datamodel for a quiz.
    """
    
    def __init__(self, title, creator_id, questions=[]):
        """ Initialises the quiz datamodel
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.creator_id = creator_id
        assert isinstance(questions, list)
        self.questions = self.addMultipleQuestions(questions)

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

    def addMultipleQuestions(self, questions):
        """ Adds a list of questions to the quiz at once
        """
        if questions:
            questionSet = []
            keys = ['question', 'options', 'answer', 'score'] 
            for question in questions:
                if isinstance(question, dict) and  all(key in question for key in keys):
                    self.__addMultipleQuestionsHelper(
                        questionSet = questionSet,
                        question = question['question'],
                        options = question['options'],
                        answer = question['answer'],
                        score = question['score']
                    )
            self.questions = questionSet
            return questionSet
        else:
            return []

    def __addMultipleQuestionsHelper(self, questionSet, question, options, answer, score=0):
        """ Adds a question to a quiz
        """
        assert isinstance(questionSet, list)
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
            "index": len(questionSet)
        }
        questionSet.append(question)

    def save(self):
        """ Returns JSON form of class.
        """
        return self.__dict__
