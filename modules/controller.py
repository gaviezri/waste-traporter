import datetime
import os
import json
from constants import CREDENTIALS_PATH, DB, DB_BACKUP_FILE, REPORT
from modules.db import DatabaseDriver
from modules.scale import ScaleDriver
from modules.sharepoint import SharePointDriver
from modules.report import ReportManager
from modules.types import WeighingPayload
from modules.ui import ScaleUI
from modules.tegrity import Tegrity
from atomic_operator import AtomicFloat

def file_modification_date(file_path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

class Controller:
    def __init__(self):
        with open(CREDENTIALS_PATH.as_posix(), 'r') as credentials_json:
            self.__sharepoint_driver = SharePointDriver(json.load(credentials_json))

        self.__report_manager = ReportManager()
        self.__db_driver = DatabaseDriver()
        # self.__scale_driver = ScaleDriver()
        self.__ui = ScaleUI(self)

        self.atomic_weight = AtomicFloat(0.0)
        
    def __task_backup_database(self):
        if Tegrity.is_backup_needed():
            
            self.__db_dump_and_upload()
            Tegrity.stamp(DB)

    def __task_create_monthly_report(self):
        if Tegrity.is_report_needed():
            
            this_month_entries = self.__db_driver.get_this_month_entries_by_type()
            report_path = self.__report_manager.create_report(this_month_entries)
            self.__sharepoint_driver.upload_file(report_path, overwrite=True)
            
            os.remove(report_path)
            Tegrity.stamp(REPORT)

    def __db_dump_and_upload(self):
        self.__db_driver.dump_database(DB_BACKUP_FILE)
        self.__sharepoint_driver.upload_file(DB_BACKUP_FILE, overwrite=True)

    def record_weighing(self, payload: WeighingPayload):
        self.__db_driver.create_record(payload)

    def get_current_weight(self):
        # return self.__scale_driver.read_stable_weight_kg()
        return 10.0

    def run(self):
        

        for task in [self.__task_backup_database, self.__task_create_monthly_report]:
            task()
        
        # ui runs in a different thread interacting with controller atomic attributes
        self.__ui.start()
