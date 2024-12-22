import unittest
from models.quiz import Quiz
from models.user import User


class TestQuizModel(unittest.TestCase):
    """ Test cases for the Quiz datamodel.
    """

    def setUp(self):
        """ Sets up some tests for the model.
        """
        self.username = "test"
        self.email = "foo@bar.com"
        self.password = "password123"

        self.question1 = "What is the Capital of Foo?"
        self.options1 = ["Lorem", "Foobar", "Bar", "Ipsum"]
        self.answer1 = "Foo"
        self.score1 = 10

        self.question2 = "What is the Capital of Bar?"
        self.options2 = ["Lorem", "Foobar", "Bar", "Ipsum"]
        self.answer2 = "Bar"
        self.score2 = 10

    def test_question_types(self):
        """ Tests if quiz has the corret data
        """
        user = User(
            username = self.username,
            email = self.email,
            password =  self.password
        )

        quiz = Quiz(
            creator_id = user.returnID(),
        )

        quiz.addQuestion(
            question = self.question1,
            options = self.options1,
            answer = self.answer1,
        )

        quiz.addQuestion(
            question = self.question2,
            options = self.options2,
            answer = self.answer2,
        )


if __name__ == '__main__':
    unittest.main()
