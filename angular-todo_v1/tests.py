from base64 import b64encode
import unittest

from playhouse.test_utils import test_database
from peewee import *

import models
import todo_app


TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([models.User, models.Todo], safe=True)


class TodoModelTests(unittest.TestCase):
    @staticmethod
    def create_todos():
        models.Todo.create(
            name="Feed the dog"
        )
        models.Todo.create(
            name="Do the dishes"
        )
        models.Todo.create(
            name="Pay the bills"
        )

    def test_todo_creation(self):
        with test_database(TEST_DB, (models.Todo,)):
            self.create_todos()
            self.assertEqual(models.Todo.select().count(), 3)

    def test_duplicate_todo_creation(self):
        with test_database(TEST_DB, (models.Todo,)):
            models.Todo.create(
                name="Feed the dog",
            )
            with self.assertRaises(IntegrityError):
                models.Todo.create(
                    name="Feed the dog",
                )


class UserModelTests(unittest.TestCase):
    @staticmethod
    def create_users():
        models.User.create_user(
            username="user1",
            password="password",
        )
        models.User.create_user(
            username="user2",
            password="password",
        )

    def test_user_creation(self):
        with test_database(TEST_DB, (models.User,)):
            self.create_users()
            self.assertEqual(models.User.select().count(), 2)
            self.assertNotEqual(models.User.select().get().password,
                                'password')

    def test_duplicate_user_creation(self):
        with test_database(TEST_DB, (models.User,)):
            self.create_users()
            with self.assertRaises(Exception):
                models.User.create_user(
                    username="user1",
                    password="password",
                )


class ResourcesTests(unittest.TestCase):
    def setUp(self):
        todo_app.app.config['TESTING'] = True
        todo_app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = todo_app.app.test_client()


class UserResourcesTests(ResourcesTests):
    def test_good_registration(self):
        data = {
            'username': 'user1',
            'password': 'password',
            'verify_password': 'password',
        }
        with test_database(TEST_DB, (models.User,)):
            rv = self.app.post('/api/v1/users', data=data)
            self.assertEqual(rv.status_code, 201)
            self.assertIn(data['username'], rv.data.decode())

    def test_bad_registration(self):
        data = {
            'username': 'user1',
            'password': 'password',
            'verify_password': 'password2',
        }
        with test_database(TEST_DB, (models.User,)):
            rv = self.app.post('/api/v1/users', data=data)
            self.assertEqual(rv.status_code, 400)

    def test_incomplete_registration1(self):
        data = {
            'username': 'user1',
            'password': 'password',
        }
        with test_database(TEST_DB, (models.User,)):
            rv = self.app.post('/api/v1/users', data=data)
            self.assertEqual(rv.status_code, 400)

    def test_incomplete_registration2(self):
        data = {
            'username': 'user1',
            'verify_password': 'password',
        }
        with test_database(TEST_DB, (models.User,)):
            rv = self.app.post('/api/v1/users', data=data)
            self.assertEqual(rv.status_code, 400)

    def test_incomplete_registration3(self):
        data = {
            'password': 'password',
            'verify_password': 'password',
        }
        with test_database(TEST_DB, (models.User,)):
            rv = self.app.post('/api/v1/users', data=data)
            self.assertEqual(rv.status_code, 400)

    def test_existing_user_registration(self):
        data = {
            'username': 'user1',
            'password': 'password',
            'verify_password': 'password',
        }
        with test_database(TEST_DB, (models.User,)):
            UserModelTests.create_users()
            rv = self.app.post('/api/v1/users', data=data)
            self.assertEqual(rv.status_code, 400)

    def test_unauthorized_get_token(self):
        with test_database(TEST_DB, (models.User,)):
            UserModelTests.create_users()
            rv = self.app.get('/api/v1/users/token')
            self.assertEqual(rv.status_code, 401)

    def test_authorized_get_token(self):
        with test_database(TEST_DB, (models.User,)):
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()

            user_password = b64encode(b"user1:password").decode("ascii")
            headers = {'Authorization': 'Basic %s' % user_password}

            rv = self.app.get('/api/v1/users/token', headers=headers)
            self.assertEqual(rv.status_code, 200)
            self.assertIn('token', rv.data.decode())
            self.assertIn(token, rv.data)


class TodoListResourcesTests(ResourcesTests):
    def test_get_todos(self):
        with test_database(TEST_DB, (models.Todo,)):
            TodoModelTests.create_todos()

            rv = self.app.get('/api/v1/todos')
            self.assertEqual(rv.status_code, 200)
            self.assertIn(models.Todo.get(models.Todo.id == 1).name,
                          rv.data.decode())
            self.assertIn(models.Todo.get(models.Todo.id == 2).name,
                          rv.data.decode())
            self.assertIn(models.Todo.get(models.Todo.id == 3).name,
                          rv.data.decode())

    def test_post_todo(self):
        data = {
            'name': 'Feed the dog',
        }
        with test_database(TEST_DB, (models.User, models.Todo)):
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()
            headers = {'Authorization': 'Token %s' % token.decode("ascii")}

            rv = self.app.post('/api/v1/todos', data=data, headers=headers)
            self.assertEqual(rv.status_code, 201)
            self.assertEqual(rv.location, 'http://localhost/api/v1/todos/1')

    def test_post_todo_unauthorized(self):
        data = {
            'name': 'Feed the dog',
        }
        with test_database(TEST_DB, (models.User, models.Todo)):
            rv = self.app.post('/api/v1/todos', data=data)
            self.assertEqual(rv.status_code, 401)

    def test_post_todo_duplicate(self):
        data = {
            'name': 'Feed the dog',
        }
        with test_database(TEST_DB, (models.User, models.Todo)):
            TodoModelTests.create_todos()
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()
            headers = {'Authorization': 'Token %s' % token.decode("ascii")}

            rv = self.app.post('/api/v1/todos', data=data, headers=headers)
            self.assertEqual(rv.status_code, 400)

    def test_post_todo_no_name(self):
        data = {}
        with test_database(TEST_DB, (models.User, models.Todo)):
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()
            headers = {'Authorization': 'Token %s' % token.decode("ascii")}

            rv = self.app.post('/api/v1/todos', data=data, headers=headers)
            self.assertEqual(rv.status_code, 400)


class TodoResourcesTest(ResourcesTests):
    def test_get_single_todo(self):
        with test_database(TEST_DB, (models.Todo,)):
            TodoModelTests.create_todos()

            rv = self.app.get('/api/v1/todos/1')
            self.assertEqual(rv.status_code, 200)
            self.assertIn(models.Todo.get(models.Todo.id == 1).name,
                          rv.data.decode())

    def test_get_single_todo_404(self):
        with test_database(TEST_DB, (models.Todo,)):
            TodoModelTests.create_todos()

            rv = self.app.get('/api/v1/todos/4')
            self.assertEqual(rv.status_code, 404)

    def test_update_todo(self):
        data = {
            "name": "Feed the cat",
            "completed": True,
        }
        with test_database(TEST_DB, (models.User, models.Todo)):
            TodoModelTests.create_todos()
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()
            headers = {'Authorization': 'Token %s' % token.decode("ascii")}
            rv = self.app.put('/api/v1/todos/1', data=data, headers=headers)
            self.assertEqual(rv.status_code, 200)
            self.assertIn(data["name"], rv.data.decode())
            self.assertEqual(rv.location, 'http://localhost/api/v1/todos/1')

    def test_update_todo_unauthorized(self):
        data = {
            "name": "Feed the cat",
            "completed": True,
        }
        with test_database(TEST_DB, (models.Todo,)):
            TodoModelTests.create_todos()
            rv = self.app.put('/api/v1/todos/1', data=data)
            self.assertEqual(rv.status_code, 401)

    def test_update_todo_404(self):
        data = {
            "name": "Feed the cat",
            "completed": True,
        }
        with test_database(TEST_DB, (models.User, models.Todo)):
            TodoModelTests.create_todos()
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()
            headers = {'Authorization': 'Token %s' % token.decode("ascii")}
            rv = self.app.put('/api/v1/todos/4', data=data, headers=headers)
            self.assertEqual(rv.status_code, 404)

    def test_delete_todo(self):
        with test_database(TEST_DB, (models.User, models.Todo)):
            TodoModelTests.create_todos()
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()
            headers = {'Authorization': 'Token %s' % token.decode("ascii")}
            rv = self.app.delete('/api/v1/todos/1', headers=headers)
            self.assertEqual(rv.status_code, 204)
            self.assertEqual(models.Todo.select().count(), 2)

    def test_delete_todo_404(self):
        with test_database(TEST_DB, (models.User, models.Todo)):
            TodoModelTests.create_todos()
            user = models.User.create_user(username="user1",
                                           password="password")
            token = user.generate_auth_token()
            headers = {'Authorization': 'Token %s' % token.decode("ascii")}
            rv = self.app.delete('/api/v1/todos/4', headers=headers)
            self.assertEqual(rv.status_code, 404)
            self.assertEqual(models.Todo.select().count(), 3)

    def test_delete_todo_unauthorized(self):
        with test_database(TEST_DB, (models.Todo,)):
            TodoModelTests.create_todos()
            rv = self.app.delete('/api/v1/todos/4')
            self.assertEqual(rv.status_code, 401)
            self.assertEqual(models.Todo.select().count(), 3)

if __name__ == '__main__':
    unittest.main()
