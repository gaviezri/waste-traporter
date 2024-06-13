import datetime
import os
import json
from constants import CREDENTIALS_PATH, DB_BACKUP_FILE
from modules.db import DatabaseDriver
from modules.sharepoint import SharePointDriver

def file_modification_date(file_path):
    # Use the earliest time among the file's creation time, modification time, and last status change time
    return datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

class Controller:
    def __init__(self):
        with open(CREDENTIALS_PATH.as_posix(), 'r') as credentials_json:
            self.__sharepoint_driver = SharePointDriver(json.load(credentials_json))
        self.__db_driver = DatabaseDriver()

    def backup_database_if_needed(self):
        last_backup_date = file_modification_date(DB_BACKUP_FILE)
        today = datetime.datetime.now()
        if not os.path.exists(DB_BACKUP_FILE) or last_backup_date.date() != today.date():  
            self.__db_driver.dump_database(DB_BACKUP_FILE)
            self.__sharepoint_driver.upload_file(DB_BACKUP_FILE)
        

                    