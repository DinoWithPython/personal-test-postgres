# tests/test_cases/test_example.py
from tests import BaseIntegrationTest

class TestDatabase(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.log_test_start()

    def tearDown(self):
        self.log_test_end()
        super().tearDown()

    def test_simple_insert(self):
        with self.transaction() as cursor:
            self.logger.info("Executing insert query")
            cursor.execute("INSERT INTO users (name, email) VALUES ('Test User', 'test@example.com')")
            
            self.logger.info("Executing select query")
            cursor.execute("SELECT * FROM users WHERE name = 'Test User'")
            result = cursor.fetchone()
            
            self.logger.info(f"Received result: {result}")
            self.assertIsNotNone(result)
            self.assertEqual(result[1], 'Test User')
            self.assertEqual(result[2], 'test@example.com')

    def test_select_all_users(self):
        self.logger.info("Testing select all users")
        with self.transaction() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            
            self.logger.info(f"Current users count: {count}")
            self.assertGreaterEqual(count, 0)

    def test_invalid_insert(self):
        self.logger.info("Testing invalid insert scenario")
        with self.assertRaises(Exception):
            with self.transaction() as cursor:
                self.logger.info("Trying to insert invalid data")
                cursor.execute("INSERT INTO users (name) VALUES ('Invalid User')")
