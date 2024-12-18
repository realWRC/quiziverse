import unittest
from models.user import User
from bcrypt import checkpw

class TestUserModel(unittest.TestCase):
    """Unittests for User model."""

    def setUp(self):
        """Set up test data before each test."""
        self.username = "test"
        self.email = "foo@bar.com"
        self.password = "password123"

    def test_user_attributes(self):
        """ Tests if User has the correct attributes.
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
        """ Test if User persists in the database. also tests
        the getByID and deleteByID methods.
        """
        user1 = User(
            username=self.username,
            email=self.email,
            password=self.password
        )
        user1.save()
        user2 = User.getByID(user1.id)
        assert user2 is not None
        self.assertEqual(user1.id, user2.id)
        self.assertEqual(user1.username, user2.username)
        self.assertEqual(user1.email, user2.email)
        self.assertEqual(user1.password, user2.password)
        User.deleteByID(user1.id)


if __name__ == "__main__":
    unittest.main()
