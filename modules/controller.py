import datetime
import os
from modules.db import DatabaseDriver
from modules.scale import ScaleDriver
from modules.sharepoint import SharePointDriver
from modules.report import ReportManager
from modules.types import AtomicFloat, WeighingPayload
from modules.ui import UIDriver
from modules.tegrity import Tegrity
from constants import DB, DB_BACKUP_FILE, REPORT

def file_modification_date(file_path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

class Controller:
    def __init__(self):

        self.__sharepoint_driver = SharePointDriver()
        self.__report_manager = ReportManager()
        self.__db_driver = DatabaseDriver()
        self.__atomic_weight = AtomicFloat()
        self.__scale_driver = ScaleDriver(self.__atomic_weight.set)
        self.__ui = UIDriver(self)
        
    def __task_backup_database(self):
        if Tegrity.is_backup_needed():
            
            self.__db_dump_and_upload()
            Tegrity.stamp(DB)

    def __task_create_monthly_report(self):
        if Tegrity.is_report_needed():
            
            this_month_entries = self.__db_driver.get_last_month_entries_by_type()
            report_path = self.__report_manager.create_report(this_month_entries)
            self.__sharepoint_driver.upload_file(report_path, overwrite=True)
            os.remove(report_path)
            self.__db_driver.delete_last_month_entries()
            Tegrity.stamp(REPORT)

    def __db_dump_and_upload(self):
        self.__db_driver.dump_database(DB_BACKUP_FILE)
        self.__sharepoint_driver.upload_file(DB_BACKUP_FILE, overwrite=True)

    def record_weighing(self, payload: WeighingPayload):
        self.__db_driver.create_record(payload)

    def get_weight(self):
        return self.__atomic_weight.get()

    def run(self):
        self.__ui.start()
        while True:
            for task in [self.__task_backup_database, self.__task_create_monthly_report]:
                task()
