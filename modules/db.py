from sqlite3 import connect
from collections import defaultdict
from datetime import datetime, date, time
from constants import DB_NAME
from dataclasses import dataclass
from modules.types import WeighingPayload

@dataclass
class WeighingEntry:
    weight: float
    date_recorded: date
    time_recorded: time

class DatabaseDriver:
    def __init__(self):
        self.__conn = connect(DB_NAME)
        self.__cursor = self.__conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS waste_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            weight REAL,
            date_recorded DATE DEFAULT CURRENT_DATE,
            time_recorded TIME DEFAULT CURRENT_TIME
        )''')
        self.__conn.commit()

    def create_record(self, payload: WeighingPayload):
        type_str = payload[0].name
        weight = payload[1]
        self.__cursor.execute("INSERT INTO waste_records (type, weight) VALUES (?, ?)", (type_str, weight))
        self.__conn.commit()

    def read_all_records(self):
        self.__cursor.execute("SELECT * FROM waste_records")
        return self.__cursor.fetchall()

    def update_record(self, record_id: int, payload: WeighingPayload):
        type_str = payload[0].name
        weight = payload[1]
        self.__cursor.execute("UPDATE waste_records SET type=?, weight=? WHERE id=?", (type_str, weight, record_id))
        self.__conn.commit()

    def delete_record(self, record_id: int):
        self.__cursor.execute("DELETE FROM waste_records WHERE id=?", (record_id,))
        self.__conn.commit()

    def dump_database(self, output_file: str):
        with open(output_file, 'w') as f:
            for line in self.__conn.iterdump():
                f.write(f"{line}\n")

    def get_this_month_entries_by_type(self):
        def process_rows(rows):
            month_entries_by_type = defaultdict(list)
            for row in rows:
                type_str, weight, date_recorded_str, time_recorded_str = row
                date_recorded = datetime.strptime(date_recorded_str, "%Y-%m-%d").date()
                time_recorded = datetime.strptime(time_recorded_str, "%H:%M:%S").time()
                entry = WeighingEntry(weight=weight, date_recorded=date_recorded, time_recorded=time_recorded)            
                # Append the entry to the list for the corresponding type
                month_entries_by_type[type_str].append(entry)
            return month_entries_by_type

        current_month = datetime.now().month
        current_year = datetime.now().year
        
        self.__cursor.execute("SELECT type, weight, date_recorded, time_recorded FROM waste_records WHERE strftime('%Y-%m', date_recorded) = ?",
                              (f"{current_year}-{current_month:02}",))
        rows = self.__cursor.fetchall()
        return process_rows(rows)