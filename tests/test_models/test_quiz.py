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
        self.assertEqual(quiz.time_limit, 0)
        self.assertEqual(quiz.total_score, 2)
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
            time_limit = 10
        )

        quiz.addMultipleQuestions(questions)

        quiz.addQuestion(
            question = self.question2,
            options = self.options2,
            answer = self.answer2,
            score = self.score2,
        )

        self.assertEqual(user.id, quiz.creator_id)
        self.assertEqual(self.title, quiz.title)
        self.assertEqual(quiz.time_limit, 10)
        self.assertEqual(quiz.total_score, 30)
        self.assertIsInstance(quiz.questions, list)
        self.assertIsInstance(quiz.questions[0], dict)
        self.assertIsInstance(quiz.questions[0]["question"], str)
        self.assertIsInstance(quiz.questions[1]["options"], list)
        self.assertTrue(self.answer1 in quiz.questions[0]["options"])
        self.assertTrue(self.answer2 in quiz.questions[1]["options"])
        self.assertEqual(quiz.questions[0]["index"], 0)
        self.assertEqual(quiz.questions[1]["index"], 1)
        self.assertEqual(quiz.questions[2]["index"], 2)

    def test_quiz_persistence(self):
        """ Tests the peristence of a quiz
        """
        questions = []
        user = User(
            username = self.username,
            email = self.email,
            password =  self.password
        )
        quizOne = Quiz(
            title = self.title,
            creator_id = user.returnID(),
            questions = questions
        )

        quizOne.addQuestion(
            question = self.question1,
            options = self.options1,
            answer = self.answer1,
        )
        quizOne.addQuestion(
            question = self.question2,
            options = self.options2,
            answer = self.answer2,
        )

        quiz_id = quizOne.quiz_id

        # Save
        quizOne.save()

        # Recreate as quizTwo
        quizTwo = Quiz.recreate(quiz_id)

        # Delete
        Quiz.delete(quiz_id)

        # Recreate quiz but should be None it does not exist
        quizThree = Quiz.recreate(quiz_id)

        assert quizTwo is not None
        self.assertIsInstance(quizTwo, Quiz)
        self.assertEqual(quizOne.quiz_id, quizTwo.quiz_id)
        self.assertEqual(quizOne.creator_id, quizTwo.creator_id)
        self.assertEqual(quizOne.title, quizTwo.title)
        self.assertEqual(quizOne.time_limit, quizTwo.time_limit)
        self.assertEqual(quizOne.total_score, quizTwo.total_score)
        self.assertEqual(quizOne.questions, quizTwo.questions)
        self.assertIsNone(quizThree)


if __name__ == '__main__':
    unittest.main()
