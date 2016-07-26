from flask import Blueprint, jsonify, make_response

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                           marshal_with, abort, url_for, inputs)

from auth import auth
import models


todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'completed': fields.Boolean,
}


def todo_or_404(todo_id):
    """Returns TODO if exists or 404 if not."""
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404, message="Todo with id {} does not exist.".format(todo_id))
    else:
        return todo


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help="No ToDo name provided",
            location=['form', 'json'],
            trim=True,
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            default=False,
            type=inputs.boolean,
            location=['form', 'json'],
        )
        super().__init__()

    def get(self):
        """GET: Returns all TODOs sorted by completed attribute and then by
        time created."""
        todos = models.Todo.select().order_by(
            models.Todo.completed, models.Todo.created_at.desc())
        return [marshal(todo, todo_fields) for todo in todos]

    @auth.login_required
    def post(self):
        """POST: Creates a new TODO."""
        args = self.reqparse.parse_args()
        try:
            todo = models.Todo.create(**args)
        except Exception as error:
            return str(error), 400
        else:
            return (marshal(todo, todo_fields), 201, {
                'Location': url_for('resources.todos.todo', todo_id=todo.id)})


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=False,
            help="No ToDo name provided",
            location=['form', 'json'],
            trim=True,
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            type=inputs.boolean,
            location=['form', 'json'],
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, todo_id):
        """GET: Returns a single TODO."""
        return todo_or_404(todo_id)

    @auth.login_required
    def put(self, todo_id):
        """PUT: Updates a single TODO."""
        args = self.reqparse.parse_args()
        cleaned_args = {key: value for (key, value) in args.items()
                        if value is not None}
        query = models.Todo.update(**cleaned_args).where(
            models.Todo.id == todo_id)
        try:
            query.execute()
        except Exception as error:
            return str(error), 400
        return (marshal(todo_or_404(todo_id), todo_fields), 200,
                {"Location": url_for('resources.todos.todo', todo_id=todo_id)})

    @auth.login_required
    def delete(self, todo_id):
        """DELETE: Deletes a single TODO."""
        todo = todo_or_404(todo_id)
        todo.delete_instance()
        return '', 204, {'Location': url_for('resources.todos.todos')}


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api, catch_all_404s=True)
api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos',
)
api.add_resource(
    Todo,
    '/todos/<int:todo_id>',
    endpoint='todo',
)
