from enum import Enum
from typing import Tuple
from datetime import date, time
from dataclasses import dataclass

@dataclass
class WeighingEntry:
    weight: float
    date_recorded: date
    time_recorded: time

class WasteType(Enum):
    """
    waste type enum 
    """
    PMD="PWD"
    PAPER="Paper"
    WASTE="Waste"

WeighingPayload = Tuple[WasteType, float]

