from enum import Enum
from typing import Tuple

class WasteType(Enum):
    """
    waste type enum 
    """
    PMD=0
    PAPER=1
    WASTE=2

WeighingPayload = Tuple[WasteType, float]
