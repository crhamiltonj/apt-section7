from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('Test'))
                self.assertDictEqual({'name': 'Test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test')
                response = client.post('/store/Test')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'Test' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test')
                response = client.delete('/store/Test')

                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('Test'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))


    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test')
                response = client.get('/store/Test')

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(response.data)
                self.assertDictEqual({'name': 'Test', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/Test')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test').save_to_db()
                ItemModel('test-item1', 19.99, 1).save_to_db()
                response = client.get('/store/Test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'Test', 'items': [{'name': 'test-item1', 'price': 19.99}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test').save_to_db()
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'Test', 'items': []}]},
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test').save_to_db()
                ItemModel('test-item1', 19.99, 1).save_to_db()
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'Test', 'items': [{'name': 'test-item1', 'price': 19.99}] }]},
                                     json.loads(response.data))
