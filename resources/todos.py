import json
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort

from models import Todo


todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'completed': fields.Boolean
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()

    def get(self):
        todos = [marshal(todo, todo_fields) for todo in Todo.select()]
        return jsonify(todos)

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = Todo.create(**args)
        return (todo, 201, {
            'Location': url_for('resources.todos.todo', id=todo.id)
        })


class TodoTask(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()

    @marshal_with(todo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            Todo.select().where(Todo.id == id).get()
        except:
            return abort(403)
        else:
            query = Todo.update(**args).where(Todo.id == id)
            query.execute()
            todo = Todo.get(Todo.id == id)
            return todo, 200

    def delete(self, id):
        try:
            Todo.select().where(Todo.id == id).get()
        except:
            return abort(403)
        else:
            query = Todo.delete().where(Todo.id == id)
            query.execute()
            return '', 204, {'Location': url_for('resources.todos.todos')}


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos'
)
api.add_resource(
    TodoTask,
    '/todos/<int:id>',
    endpoint='todo'
)
