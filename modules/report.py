import pandas as pd
from typing import Dict, List
from datetime import datetime
from modules.types import WasteType, WeighingEntry
from constants import PROJECT_ROOT

class ReportManager:
    
    WASTE_TYPE = "Waste Type"
    TOTAL_KG = "Total Kg"

    def create_report(self, weighing_entries: Dict[WasteType ,List[WeighingEntry]]) -> str:
        now = datetime.now()
        report_path = PROJECT_ROOT / f"{now.year}-{now.month}.xlsx" 
        df = pd.DataFrame(columns=[self.WASTE_TYPE, self.TOTAL_KG])
        
        for waste_type, entries in weighing_entries:
            total_kg = sum(entry.weight for entry in entries)
            df = df.append({self.WASTE_TYPE: waste_type, self.TOTAL_KG: total_kg}, ignore_index=True)

        df.to_excel(report_path, index=False)

        return report_path



# TEST
def test():
    now = datetime.now().date()
    entries = {
            WasteType.PMD.value : [WeighingEntry(100, now.date(), now.time())],
            WasteType.PAPER.value : [WeighingEntry(150, now.date(), now.time())],
            WasteType.WASTE.value : [WeighingEntry(200, now.date(), now.time())],
        }

    ReportManager().create_report(entries)