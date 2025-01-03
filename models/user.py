import bcrypt
import uuid
from datetime import datetime, timezone
from models import db
from flask_login import UserMixin

class User(UserMixin):
    """ Defines the User model for the quiziverse application
    """

    def __init__(
        self, username, email, password, user_id=str(uuid.uuid4()),
        other={"registed_at": datetime.now(timezone.utc)}
    ):
        """ Initialises User object
        """
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
        db.users.insert_one(self.__dict__)

    def delete(self):
        """ Deletes self from storage.
        """
        db.users.delete_one({"id": self.id})

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
        data = db.users.find_one({"id": user_id})
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
        data = db.users.find_one({"username": username})
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
        data = db.users.find_one({"email": email})
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
        db.users.delete_one({"id": user_id})
