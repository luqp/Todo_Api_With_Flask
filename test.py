import unittest
from peewee import SqliteDatabase

import app
from models import Todo


TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

    def test_post(self):
        with TEST_DB.bind_ctx((Todo,)):
            TEST_DB.create_tables((Todo,), safe=True)
            data = self.client.post('/api/v1/todos', data=dict(
                name='Please do not write',
                completed=False
            ))
            self.assertEqual(data.status_code, 201)

    def test_get(self):
        with TEST_DB.bind_ctx((Todo,)):
            TEST_DB.create_tables((Todo,), safe=True)
            data = self.client.get('/api/v1/todos')
            self.assertEqual(data.status_code, 200)

    def test_put(self):
        with TEST_DB.bind_ctx((Todo,)):
            TEST_DB.create_tables((Todo,), safe=True)
            data = self.client.post('/api/v1/todos', data=dict(
                name='Please do not write',
                completed=False
            ))
            todo_id = data.location.split('/')[-1]
            data = self.client.put(f'/api/v1/todos/{todo_id}', data=dict(
                name='Please do not write',
                completed=False
            ))
            self.assertEqual(data.status_code, 200)

    def test_invalid_id_on_update(self):
        with TEST_DB.bind_ctx((Todo,)):
            TEST_DB.create_tables((Todo,), safe=True)
            data = self.client.put(f'/api/v1/todos/1', data=dict(
                name='Please do not write',
                completed=False
            ))
            self.assertEqual(data.status_code, 403)

    def test_delete(self):
        with TEST_DB.bind_ctx((Todo,)):
            TEST_DB.create_tables((Todo,), safe=True)
            data = self.client.post('/api/v1/todos', data=dict(
                name='Please do not write',
                completed=False
            ))
            todo_id = data.location.split('/')[-1]
            data = self.client.delete(f'/api/v1/todos/{todo_id}')
            self.assertEqual(data.status_code, 204)

    def test_invalid_id_on_delete(self):
        with TEST_DB.bind_ctx((Todo,)):
            TEST_DB.create_tables((Todo,), safe=True)
            data = self.client.delete(f'/api/v1/todos/1')
            self.assertEqual(data.status_code, 403)


if __name__ == '__main__':
    unittest.main()
