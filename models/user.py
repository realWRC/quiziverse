import bcrypt
import uuid
from datetime import datetime, timezone
from models import usersCollection, resultsCollection
from flask_login import UserMixin

class User(UserMixin):
    """ Defines the User model for the quiziverse application
    """

    def __init__(
        self, username, email, password, user_id=None,
        other={"registed_at": datetime.now(timezone.utc)}
    ):
        """ Initialises User object
        """
        if user_id is None:
            user_id = str(uuid.uuid4())
        self.id = user_id
        self.username = username
        self.email = email
        if isinstance(password, str):
            self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        else:
            self.password = password
        self.other = other

    def save(self):
        """ Commits user to database
        """
        usersCollection.insert_one(self.__dict__)

    def delete(self):
        """ Deletes self from storage.
        """
        usersCollection.delete_one({"id": self.id})

    def checkpwd(self, password):
        """ Checks if given password matches stored password.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def returnID(self):
        """ Returns the users ID.
        """
        return self.id

    @staticmethod
    def getByID(user_id):
        """ Gets user
        """
        data = usersCollection.find_one({"id": user_id})
        if data:
            return User(
                user_id = data["id"],
                username = data["username"],
                email = data["email"],
                password = data["password"],
                other = data["other"]
            )

    @staticmethod
    def getByUsername(username):
        """ Gets the user using username
        """
        data = usersCollection.find_one({"username": username})
        if data:
            return User(
                user_id = data["id"],
                username = data["username"],
                email = data["email"],
                password = data["password"],
                other = data["other"]
            )

    @staticmethod
    def getByEmail(email):
        """ Gets the user by email
        """
        data = usersCollection.find_one({"email": email})
        if data:
            return User(
                user_id = data["id"],
                username = data["username"],
                email = data["email"],
                password = data["password"],
                other = data["other"]
            )
    @staticmethod
    def deleteByID(user_id):
        """ Deletes user using ID
        """
        usersCollection.delete_one({"id": user_id})
        resultsCollection.delete_many({"user_id": user_id})
