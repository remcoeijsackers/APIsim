from dataclasses import dataclass
from typing import Any

@dataclass
class request_unit:
    url: str
    mode: str
    time: float
    status: str
    outcome: Any = None
    body: Any = None
