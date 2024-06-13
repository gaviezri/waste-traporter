import datetime
import os
import json
from constants import CREDENTIALS_PATH, DB, DB_BACKUP_FILE, REPORT
from modules.db import DatabaseDriver
from modules.sharepoint import SharePointDriver
from modules.report import ReportManager
from modules.types import WeighingPayload
from modules.ui import ScaleUI
from modules.tegrity import Tegrity
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
        # new month and a report for this month have not been produced yet
        # single method of report manager
        if Tegrity.is_report_needed():
            this_month_entries = self.__db_driver.get_this_month_entries_by_type()
            report_path = self.__report_manager.create_report(this_month_entries)
            self.__sharepoint_driver.upload_file(report_path, overwrite=True)
            Tegrity.stamp(REPORT)

    def __db_dump_and_upload(self):
        self.__db_driver.dump_database(DB_BACKUP_FILE)
        self.__sharepoint_driver.upload_file(DB_BACKUP_FILE, overwrite=True)

    def __backup_database_if_needed(self):
        if Tegrity.is_backup_needed():
            self.__db_dump_and_upload()
            Tegrity.stamp(DB)

    def run(self):
        
        def backup_task():
            while True:
                self.__backup_database_if_needed()
        
        def report_task():
            while True:
                self.__create_monthly_report_if_needed()

        for task in [report_task, backup_task]:
            Thread(target=task).start()


        self.__ui.start()


