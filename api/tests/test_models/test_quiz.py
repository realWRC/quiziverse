import unittest
from models.quiz import Quiz
from models.user import User


class TestQuizModel(unittest.TestCase):
    """ Test cases for the Quiz datamodel.
    """

    def setUp(self):
        """ Sets up some tests for the model.
        """
        self.title = "Capital Cities Quiz."

        self.username = "test"
        self.email = "foo@bar.com"
        self.password = "password123"

        self.question1 = "What is the Capital of Foo?"
        self.options1 = ["Lorem", "Foobar", "Bar", "Ipsum"]
        self.answer1 = "Ipsum"
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
            title = self.title,
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

        self.assertEqual(user.id, quiz.creator_id)
        self.assertEqual(self.title, quiz.title)
        self.assertIsInstance(quiz.questions, list)
        self.assertIsInstance(quiz.questions[0], dict)
        self.assertIsInstance(quiz.questions[0]["question"], str)
        self.assertIsInstance(quiz.questions[1]["options"], list)
        self.assertTrue(self.answer1 in quiz.questions[0]["options"])
        self.assertTrue(self.answer2 in quiz.questions[1]["options"])
        self.assertEqual(quiz.questions[0]["index"], 0)
        self.assertEqual(quiz.questions[1]["index"], 1)

    def test_add_multiple_questions(self):
        """ Tests if the addMultipleQuestions method works
        """
        questions = [
            {
                "question": self.question1,
                "options": self.options1,
                "answer": self.answer1,
                "score": self.score1
            },
            {
                "question": self.question2,
                "options": self.options2,
                "answer": self.answer2,
                "score": self.score2
            },
        ]
        user = User(
            username = self.username,
            email = self.email,
            password =  self.password
        )
        quiz = Quiz(
            title = self.title,
            creator_id = user.returnID(),
            questions = questions
        )

        self.assertEqual(user.id, quiz.creator_id)
        self.assertEqual(self.title, quiz.title)
        self.assertIsInstance(quiz.questions, list)
        self.assertIsInstance(quiz.questions[0], dict)
        self.assertIsInstance(quiz.questions[0]["question"], str)
        self.assertIsInstance(quiz.questions[1]["options"], list)
        self.assertTrue(self.answer1 in quiz.questions[0]["options"])
        self.assertTrue(self.answer2 in quiz.questions[1]["options"])

        quiz.addQuestion(
            question = self.question2,
            options = self.options2,
            answer = self.answer2,
        )

        self.assertEqual(quiz.questions[0]["index"], 0)
        self.assertEqual(quiz.questions[1]["index"], 1)
        self.assertEqual(quiz.questions[2]["index"], 2)


if __name__ == '__main__':
    unittest.main()
