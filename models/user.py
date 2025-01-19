import bcrypt
import uuid
from datetime import datetime, timezone
from models import usersCollection, resultsCollection
from flask_login import UserMixin


class User(UserMixin):
    """ 
    Defines the User model for the quiziverse application.

    Attributes:
        id(str): Unique identifier for the user
        username(str): The users username
        email(str): The users email address
        password(str): The users encrypted password
        other(dict): Place holder for adding new fields
    """

    def __init__(
        self, username, email, password, user_id=None,
        other={"registed_at": datetime.now(timezone.utc)}
    ):
        """ 
        Initialises a User object instance.

        Args:
            id(str): Unique identifier for the user
            username(str): The users username
            email(str): The users email address
            password(str): The users encrypted password
            other(dict): Place holder for adding new fields
        """
        if user_id is None:
            user_id = str(uuid.uuid4())
        self.id = user_id
        self.username = username
        self.email = email
        if isinstance(password, str):
            self.password = bcrypt.hashpw(
                    password.encode('utf-8'), bcrypt.gensalt()
                )
        else:
            self.password = password
        self.other = other

    def save(self):
        """
        Commits/saves the User object instance to the database
        as a dictionary.
        """
        usersCollection.insert_one(self.__dict__)

    def delete(self):
        """ 
        Deletes current User object instance from the database.
        """
        usersCollection.delete_one({"id": self.id})

    def checkpwd(self, password):
        """
        Checks if given password matches stored password.

        Args:
            password(str): The plain text password for verification
        Returns:
            bool: True is the password matches the stored password
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def returnID(self):
        """ 
        Returns the id of a User object instance.
        """
        return self.id

    @staticmethod
    def getByID(user_id):
        """
        Creates a User object instance using data stored in the
        database based on the users id.

        Args:
            user_id(str): The unique identifier of the user
        """
        data = usersCollection.find_one({"id": user_id})
        if data:
            return User(
                user_id=data["id"],
                username=data["username"],
                email=data["email"],
                password=data["password"],
                other=data["other"]
            )

    @staticmethod
    def getByUsername(username):
        """
        Creates a User object instance using data stored in the
        database based on the users username.

        Args:
            username(str): The username of a given user
        """
        data = usersCollection.find_one({"username": username})
        if data:
            return User(
                user_id=data["id"],
                username=data["username"],
                email=data["email"],
                password=data["password"],
                other=data["other"]
            )

    @staticmethod
    def getByEmail(email):
        """
        Creates a User object instance using data stored in the
        database based on the users email.

        Args:
            email(str): The email of a given user
        """
        data = usersCollection.find_one({"email": email})
        if data:
            return User(
                user_id=data["id"],
                username=data["username"],
                email=data["email"],
                password=data["password"],
                other=data["other"]
            )

    @staticmethod
    def deleteByID(user_id):
        """ 
        Deletes the data for a user given a user id.

        Args:
            user_id(str): The unique identifier of the user
        """
        usersCollection.delete_one({"id": user_id})
        resultsCollection.delete_many({"user_id": user_id})
