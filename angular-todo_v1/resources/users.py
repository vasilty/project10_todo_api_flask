from flask import Blueprint, jsonify

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                           marshal_with, abort, url_for, inputs)

import models

user_fields = {
    'username': fields.String
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help="No username provided",
            location=['form', 'json'],
            trim=True,
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help="No password provided",
            location=['form', 'json'],
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help="No password verification provided",
            location=['form', 'json'],
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            try:
                user = models.User.create_user(**args)
            except Exception as error:
                return {'error': str(error)}, 400
            return marshal(user, user_fields), 201
        return ({'error': 'Password and password verification do not match'},
                400)

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users',
)
