import sqlite3
from enum import Enum
from typing import Tuple
from constants import DB_NAME
from modules.types import WeighingPayload



class DatabaseDriver:
    def __init__(self):
        self.__conn = sqlite3.connect(DB_NAME)
        self.__cursor = self.__conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS waste_records (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    type TEXT,
                                    weight REAL
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