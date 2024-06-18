from enum import Enum
from typing import Tuple
from datetime import date, time
from threading import Lock
from dataclasses import dataclass

@dataclass
class WeighingEntry:
    weight: float
    date_recorded: date
    time_recorded: time

class TrashType(Enum):
    """
    waste type enum 
    """
    PMD="PWD"
    PAPER="Paper"
    WASTE="Waste"

WeighingPayload = Tuple[TrashType, float]

class AtomicFloat:
    def __init__(self):
        self.__lock = Lock()
        self.__value = 0.0

    def get(self):
        return self.__value
    
    def set(self, new_value):
        assert isinstance(new_value, float), "new_value must be a float"
        with self.__lock:
            self.__value = new_value

