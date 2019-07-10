import datetime
from peewee import *

DATABASE = SqliteDatabase('todoList.sqlite')


class Todo(Model):
    name = CharField()
    completed = BooleanField(default=False)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
