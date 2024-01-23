import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId


class ReminderManager:
    """
    A class for managing reminders in a MongoDB database.

    Parameters:
    - db_uri (str): The MongoDB connection URI.
    - db_port (str): The MongoDB port.
    - db_name (str): The name of the MongoDB database.
    - db_user (str): The MongoDB root user.
    - db_password (str): The MongoDB root password

    Usage:
    with ReminderManager() as reminder_manager:
        reminder_manager.save_reminder('some_text', datetime.utcnow())
        print(reminder_manager.get_reminder_by_id('reminder_id'))
        print(reminder_manager.get_all_reminders())
        reminder_manager.delete_reminder('reminder_id')
    """
    default_db_host = os.getenv("DB_HOST", "localhost")
    default_db_port = os.getenv("DB_PORT", '27017')
    default_db_name = os.getenv("DB_NAME", "reminders_db")
    default_db_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    default_db_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

    def __init__(self, db_host: str = default_db_host, db_port: str = default_db_port, db_name: str = default_db_name,
                 db_user: str = default_db_user, db_password: str = default_db_password):

        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

        if self.db_user and self.db_password:
            self.db_uri = f"mongodb://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        else:
            self.db_uri = f"mongodb://{self.db_host}:{self.db_port}/{self.db_name}"

    def __enter__(self):
        self.client = MongoClient(self.db_uri)
        self.db = self.client[self.db_name]

        if self.default_db_name not in self.db.list_collection_names():
            self.db.create_collection(self.default_db_name)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

    def save_reminder(self, reminder_text: str, reminder_time: datetime) -> None:
        """
        Saves a reminder to the database and updates the reminders collection
        :param reminder_text: reminder text
        :param reminder_time: reminder time
        :return: None
        """
        reminder = {
            'text': reminder_text,
            'time': reminder_time,
        }
        self.db.reminders.insert_one(reminder)

    def get_all_reminders(self) -> list | None:
        """
        Returns a list of all reminders in the collection
        :return: list or None
        """
        try:
            return list(self.db.reminders.find())
        except Exception as ex:
            print(f"Error fetching reminders: {ex}")
            return None

    def get_reminder_by_id(self, reminder_id) -> dict | None:
        """
        Fetches a reminder by its _id and returns the reminder
        :param reminder_id: reminder _id
        :return: dict or None
        """
        try:
            return self.db.reminders.find_one({'_id': ObjectId(reminder_id)})
        except Exception as ex:
            print(f"Error fetching reminder by _id: {ex}")
            return None

    def delete_reminder(self, reminder_id) -> None:
        """
        Deletes a reminder by its _id
        :param reminder_id:
        :return: None if reminder not found
        """
        try:
            self.db.reminders.delete_one({'_id': ObjectId(reminder_id)})
        except Exception as ex:
            print(f"Error deleting reminder: {ex}")
            return None

    def get_reminder_id_by_text(self, text: str) -> str | None:
        """
        Fetches a reminder by its text and returns the reminder
        :param text: reminder text
        :return: _id or None if reminder not found
        """
        try:
            return self.db.reminders.find_one(
                {
                    'text': text
                }
            ).get('_id')
        except Exception as ex:
            print(f"Error getting reminder by text: {ex}")
            return None

# if __name__ == '__main__':
#     with ReminderManager() as reminder_manager:
#
#         date_obj = datetime.now().isoformat()
#
#         reminder_manager.save_reminder('Check new features', date_obj)
#
#         reminder_id = reminder_manager.get_reminder_id_by_text('Check new features')
#
#         print(reminder_manager.get_reminder_by_id(reminder_id))
#         print()
#         print(reminder_manager.get_all_reminders())
#         # reminder_manager.delete_reminder(reminder_id)
