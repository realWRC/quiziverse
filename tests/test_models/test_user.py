#!/usr/bin/env python3
"""
Unittests for the User Model
"""

import unittest
from models.user import User
from bcrypt import checkpw


class TestUserModel(unittest.TestCase):
    """
    Unittests for User model using unittest.TestCase class.
    """

    def setUp(self):
        """
        Set up test data before each test.
        """
        self.username = "unittesttest"
        self.email = "unitestfoo@bar.com"
        self.password = "unitestpassword123"

    def tearDown(self):
        """
        Clean up after tests by deleting the user
        from the test user from database.
        """
        user = User.getByUsername(self.username)
        if user:
            user.delete()

    def test_user_attributes(self):
        """
        Tests if User attributes have the correct types.
        """
        user = User(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertIsInstance(user.id, str)
        self.assertIsInstance(user.username, str)
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.password, bytes)

        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        assert isinstance(user.password, bytes)
        self.assertTrue(checkpw(self.password.encode('utf-8'), user.password))

    def test_user_persistence(self):
        """
        Test if User persists in the database thus the
        getByID and deleteByID methods.
        """
        user1 = User(
            username=self.username,
            email=self.email,
            password=self.password
        )
        user1.save()
        user2 = User.getByID(user1.id)
        User.deleteByID(user1.id)

        assert user2 is not None
        self.assertEqual(user1.id, user2.id)
        self.assertEqual(user1.username, user2.username)
        self.assertEqual(user1.email, user2.email)
        self.assertEqual(user1.password, user2.password)

    def test_get_user_by_username(self):
        """
        Tests if user can be retrieved by username.
        """
        user1 = User(
            username=self.username,
            email=self.email,
            password=self.password
        )
        user1.save()
        user2 = User.getByUsername(user1.username)
        User.deleteByID(user1.id)

        assert user2 is not None
        self.assertEqual(user1.id, user2.id)
        self.assertEqual(user1.username, user2.username)
        self.assertEqual(user1.email, user2.email)
        self.assertEqual(user1.password, user2.password)

    def test_get_user_by_email(self):
        """
        Tests is user can be retrieved by email
        """
        user1 = User(
            username=self.username,
            email=self.email,
            password=self.password
        )
        user1.save()
        user2 = User.getByEmail(user1.email)
        User.deleteByID(user1.id)

        assert user2 is not None
        self.assertEqual(user1.id, user2.id)
        self.assertEqual(user1.username, user2.username)
        self.assertEqual(user1.email, user2.email)
        self.assertEqual(user1.password, user2.password)


if __name__ == "__main__":
    unittest.main()
