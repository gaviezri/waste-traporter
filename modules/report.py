from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
from typing import Dict, List
from datetime import datetime
from modules.types import WasteType, WeighingEntry
from constants import PROJECT_ROOT

class ReportManager:
    
    WASTE_TYPE = "Waste Type"
    TOTAL_KG = "Total Kg"
    DATE = "Date"
    WEIGHT = "Weight"

    def __init__(self):
        self.workbook = None

    def create_report(self, weighing_entries: Dict[WasteType ,List[WeighingEntry]]) -> str:
        now = datetime.now()
        report_path = PROJECT_ROOT / f"{now.year}-{now.month}.xlsx" 

        type_to_df = {}
        
        for _type in [WasteType.WASTE, WasteType.PMD, WasteType.PAPER]:
           type_to_df[_type] = self.__create_df_from_entries(weighing_entries[_type.value])

        self.workbook = Workbook(write_only=True)

        for _type, df in type_to_df.items():
            self.__add_sheet(df, _type.value)
        
        summary_df = self.__create_summary_df(weighing_entries)
        self.__add_sheet(summary_df, "Summary")

        self.workbook.save(report_path)

        return report_path

    def __create_summary_df(self, weighing_entries: Dict[WasteType ,List[WeighingEntry]]):
        df = DataFrame(columns=[self.WASTE_TYPE, self.TOTAL_KG])
        
        for waste_type, entries in weighing_entries.items():
            total_kg = sum(entry.weight for entry in entries)
            df.loc[len(df)] = {self.WASTE_TYPE: waste_type, self.TOTAL_KG: total_kg}
        
        return df
    
    def __create_df_from_entries(self, entries: List[WeighingEntry]):
        df = DataFrame(columns=[self.DATE, self.WEIGHT])

        for entry in sorted(entries, key=lambda entry: (entry.date_recorded, entry.time_recorded)):
            datetime_str = entry.date_recorded.strftime("[%d] @ ") + entry.time_recorded.strftime("%H:%M")
            df.loc[len(df)] = {self.DATE: datetime_str, self.WEIGHT: entry.weight}
        
        return df
    
    def __add_sheet(self, df, sheet_name: str):
        sheet = self.workbook.create_sheet(title=sheet_name)

        for i, row in enumerate(dataframe_to_rows(df, index=True, header=True)):
            if i != 1:
                sheet.append(row)

        tab = Table(displayName=sheet_name, ref=f"A1:{chr(65 + len(df.columns))}{len(df) + 1}")
        tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                                            showLastColumn=False, showRowStripes=True, showColumnStripes=True)
        sheet.add_table(tab)

# TEST
def test():
    now = datetime.now()
    entries = {
            WasteType.PMD.value : [WeighingEntry(100, now.date(), now.time())],
            WasteType.PAPER.value : [WeighingEntry(150, now.date(), now.time())],
            WasteType.WASTE.value : [WeighingEntry(200, now.date(), now.time())],
        }

    ReportManager().create_report(entries)