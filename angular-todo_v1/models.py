import datetime
from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *


DATABASE = SqliteDatabase('todos.sqlite')
HASHER = PasswordHasher()
SECRET_KEY = 'AHD%#274%dfna2$!l95fDBkrgnkr873^%@fk'


class Todo(Model):
    name = CharField(unique=True)
    completed = BooleanField(default=False)
    edited = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class User(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password, **kwargs):
        try:
            cls.select().where(cls.username ** username).get()
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that username already exists")

    @staticmethod
    def verify_auth_token(token):
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
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.password, password)

    def generate_auth_token(self, expires=3600):
        serializer = Serializer(SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
