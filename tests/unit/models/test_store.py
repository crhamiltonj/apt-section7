from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_can_create_store(self):
        store = StoreModel('Test')

        self.assertEqual(store.name, 'Test',
                         "The name of the store after creation does not equal the contstructor argument.")
