import os
from .report import ReportManager
from .sharepoint import SharePointDriver
from .db import DatabaseDriver

def create_defacto_report(month, year):
    db_driver = DatabaseDriver()
    sharepoint_driver = SharePointDriver()
    report_manager = ReportManager()

    entries = db_driver.get_specified_date_entries_by_type(month, year)
    report_path = report_manager.create_report(entries)
    sharepoint_driver.upload_file(report_path)
    os.remove(report_path)
    db_driver.delete_specified_date_entries(month, year)
