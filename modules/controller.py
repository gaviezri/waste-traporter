import datetime
import os
import json
from constants import CREDENTIALS_PATH, DB_BACKUP_FILE
from modules.db import DatabaseDriver
from modules.sharepoint import SharePointDriver
from modules.report import ReportManager
from modules.types import WeighingPayload
from modules.ui import ScaleUI
from threading import Thread

def file_modification_date(file_path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

class Controller:
    def __init__(self):
        with open(CREDENTIALS_PATH.as_posix(), 'r') as credentials_json:
            self.__sharepoint_driver = SharePointDriver(json.load(credentials_json))
        self.__db_driver = DatabaseDriver()
        self.__report_manager = ReportManager()
        self.__ui = ScaleUI(self)

    def record_weighing(self, payload: WeighingPayload):
        self.__db_driver.create_record(payload)

    def __create_monthly_report_if_needed(self):
        this_month_entries = self.__db_driver.get_this_month_entries_by_type()
        report_path = self.__report_manager.create_report(this_month_entries)
        self.__sharepoint_driver.upload_file(report_path)


    def __db_dump_and_upload(self):
        self.__db_driver.dump_database(DB_BACKUP_FILE)
        self.__sharepoint_driver.upload_file(DB_BACKUP_FILE, overwrite=True)

    def __backup_database_if_needed(self):
        last_backup_date = file_modification_date(DB_BACKUP_FILE)
        today = datetime.datetime.now()
        if not os.path.exists(DB_BACKUP_FILE) or last_backup_date.date() != today.date():
            self.__db_dump_and_upload()

    def run(self):
        def backup_task():
            while True:
                self.__backup_database_if_needed()
        def report_task():
            while True:
                self.__create_monthly_report_if_needed()
        Thread(target=backup_task).start()


        self.__ui.start()


