#!/usr/bin/env python3
"""
Unittests of the Quiz class.
"""

import unittest
from models.quiz import Quiz
from models.user import User


class TestQuizModel(unittest.TestCase):
    """
    Unittest for Quiz class using unittest.TestCase.
    """

    def setUp(self):
        """
        Sets up some tests for the Quiz model.
        """
        self.title = "Capital Cities Quiz."
        self.description = "This is lorem description"

        self.username = "test"
        self.email = "foo@bar.com"
        self.password = "password123"
        self.longdescription = """Lorem ipsum dolor sit amet consectetur
        adipisicing elit. Autem totam officiis amet, velit tempore assumenda.
        Incidunt natus ex iusto praesentium ab officiis numquam cumque
        doloribus ducimus odio suscipit laboriosam tenetur at dignissimos
        dolore eveniet aliquam earum quam, sequi, odit repudiandae."""

        self.question1 = "What is the Capital of Foo?"
        self.options1 = ["Lorem", "Foobar", "Bar", "Ipsum"]
        self.answer1 = "Ipsum"
        self.score1 = 10

        self.question2 = "What is the Capital of Bar?"
        self.options2 = ["Lorem", "Foobar", "Bar", "Ipsum"]
        self.answer2 = "Bar"
        self.score2 = 10

    def test_question_types(self):
        """
        Tests if quiz has the corret data types
        """
        user = User(
            username=self.username,
            email=self.email,
            password=self.password
        )
        quiz = Quiz(
            title=self.title,
            creator_id=user.returnID(),
            description=self.description
        )
        quiz.addQuestion(
            question=self.question1,
            options=self.options1,
            answer=self.answer1,
        )
        quiz.addQuestion(
            question=self.question2,
            options=self.options2,
            answer=self.answer2,
        )

        self.assertEqual(user.id, quiz.creator_id)
        self.assertEqual(self.title, quiz.title)
        self.assertEqual(quiz.time_limit, 0)
        self.assertEqual(quiz.total_score, 2)
        self.assertIsInstance(quiz.description, str)
        self.assertIsInstance(quiz.category, str)
        self.assertIsInstance(quiz.questions, list)
        self.assertIsInstance(quiz.questions[0], dict)
        self.assertIsInstance(quiz.questions[0]["question"], str)
        self.assertIsInstance(quiz.questions[1]["options"], list)
        self.assertTrue(self.answer1 in quiz.questions[0]["options"])
        self.assertTrue(self.answer2 in quiz.questions[1]["options"])
        self.assertEqual(quiz.questions[0]["index"], 0)
        self.assertEqual(quiz.questions[1]["index"], 1)

    def test_add_multiple_questions(self):
        """
        Tests if the addMultipleQuestions method works as expected
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
            username=self.username,
            email=self.email,
            password=self.password
        )
        quiz = Quiz(
            title=self.title,
            creator_id=user.returnID(),
            description=self.description,
            time_limit=10
        )

        quiz.addMultipleQuestions(questions)

        quiz.addQuestion(
            question=self.question2,
            options=self.options2,
            answer=self.answer2,
            score=self.score2,
        )

        self.assertEqual(user.id, quiz.creator_id)
        self.assertEqual(self.title, quiz.title)
        self.assertEqual(quiz.time_limit, 10)
        self.assertEqual(quiz.total_score, 30)
        self.assertIsInstance(quiz.description, str)
        self.assertIsInstance(quiz.category, str)
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
        """
        Tests the peristence of a quiz in the database.
        Uses:
            Quiz.addQuestion()
            Quiz.recreate()
            Quiz.delete()
        """
        questions = []
        user = User(
            username=self.username,
            email=self.email,
            password=self.password
        )
        quizOne = Quiz(
            title=self.title,
            creator_id=user.returnID(),
            description=self.description,
            questions=questions
        )

        quizOne.addQuestion(
            question=self.question1,
            options=self.options1,
            answer=self.answer1,
        )
        quizOne.addQuestion(
            question=self.question2,
            options=self.options2,
            answer=self.answer2,
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
        self.assertEqual(quizOne.description, quizTwo.description)
        self.assertEqual(quizOne.category, quizTwo.category)
        self.assertEqual(quizOne.time_limit, quizTwo.time_limit)
        self.assertEqual(quizOne.total_score, quizTwo.total_score)
        self.assertEqual(quizOne.questions, quizTwo.questions)
        self.assertIsNone(quizThree)

    def test_db_quiz_data_types(self):
        """
        Tests the types for quizzes retried from database and
        the addMultipleQuestions method.
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
            username=self.username,
            email=self.email,
            password=self.password
        )
        quiz = Quiz(
            title=self.title,
            creator_id=user.returnID(),
            description=self.description,
            time_limit=10
        )

        quiz.addMultipleQuestions(questions)
        quiz.save()

        quiz_db = Quiz.get(quiz.quiz_id)
        Quiz.delete(quiz.quiz_id)

        assert quiz_db is not None
        self.assertIsInstance(quiz_db['questions'], list)
        self.assertIsInstance(quiz_db['questions'][0], dict)
        self.assertIsInstance(quiz_db['questions'][0]['question'], str)
        self.assertIsInstance(quiz_db['questions'][1]['options'], list)


if __name__ == '__main__':
    unittest.main()
