from enum import Enum
from typing import Tuple

class WasteType(Enum):
    """
    waste type enum 
    """
    PMD="PWD"
    PAPER="Paper"
    WASTE="Waste"

WeighingPayload = Tuple[WasteType, float]
