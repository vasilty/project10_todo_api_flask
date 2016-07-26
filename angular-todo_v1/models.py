import datetime
from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *


DATABASE = SqliteDatabase('todos.sqlite')
HASHER = PasswordHasher()
SECRET_KEY = 'AHD%#274%dfna2$!l95fDBkrgnkr873^%@fk'


class Todo(Model):
    """Todo model class."""
    name = CharField(unique=True)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class User(Model):
    """User model class."""
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        """Creates a user."""
        try:
            cls.select().where(cls.username ** username).get()
        # If user with that username doesn't exist, create a user.
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that username already exists")

    @staticmethod
    def verify_auth_token(token):
        """Verifies an authentication token."""
        serializer = Serializer(SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.get(User.id == data['id'])
            return user

    @staticmethod
    def set_password(password):
        """Sets user password."""
        return HASHER.hash(password)

    def verify_password(self, password):
        """Verifies user password."""
        return HASHER.verify(self.password, password)

    def generate_auth_token(self, expires=3600):
        """Generates authentication token."""
        serializer = Serializer(SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
