import unittest
from datetime import datetime

from pymongo import MongoClient

from app.database.db import ReminderManager


class TestReminderManager(unittest.TestCase):

    def setUp(self):
        # Set test environment variables
        self.test_db_host = 'localhost'
        self.test_db_port = '27017'
        self.test_db_name = 'test_reminders_db'

        self.reminder_manager = ReminderManager(
            db_host=self.test_db_host,
            db_port=self.test_db_port,
            db_name=self.test_db_name,
        )

    def tearDown(self):
        # Drop the test database after each test
        with MongoClient(self.reminder_manager.db_uri) as client:
            client.drop_database(self.test_db_name)

    def test_save_and_get_reminder(self):
        reminder_text = 'Test reminder'
        reminder_time = datetime.now().strftime('%Y-%m-%d %H:%M')

        with self.reminder_manager as manager:
            manager.save_reminder(reminder_text, reminder_time)
            reminders = manager.get_all_reminders()

            self.assertEqual(len(reminders), 1)
            saved_reminder = reminders[0]

            self.assertEqual(saved_reminder['text'], reminder_text)

    def test_get_reminder_by_id(self):
        reminder_text = 'Test reminder'
        reminder_time = datetime.now().strftime('%Y-%m-%d %H:%M')

        with self.reminder_manager as manager:
            manager.save_reminder(reminder_text, reminder_time)
            reminders = manager.get_all_reminders()

            saved_reminder_id = manager.get_reminder_by_id(reminders[0]['_id'])

            self.assertIsNotNone(saved_reminder_id)

    def test_delete_reminder(self):
        reminder_text = 'Test reminder'
        reminder_time = datetime.now().strftime('%Y-%m-%d %H:%M')

        with self.reminder_manager as manager:
            manager.save_reminder(reminder_text, reminder_time)
            reminders = manager.get_all_reminders()

            saved_reminder_id = reminders[0]['_id']
            manager.delete_reminder(saved_reminder_id)

            deleted_reminder = manager.get_reminder_by_id(saved_reminder_id)

            self.assertIsNone(deleted_reminder)

    def test_get_reminder_id_by_text(self):
        reminder_text = 'Test reminder'
        reminder_time = datetime.now().strftime('%Y-%m-%d %H:%M')

        with self.reminder_manager as manager:
            manager.save_reminder(reminder_text, reminder_time)

            saved_reminder_id = manager.get_reminder_id_by_text(reminder_text)

            self.assertIsNotNone(saved_reminder_id)


if __name__ == '__main__':
    unittest.main()
