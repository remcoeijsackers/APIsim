from dataclasses import dataclass
from typing import Any

@dataclass
class request_unit:
    url: str
    mode: str

@dataclass 
class response_unit:
    url: str
    value: str
    mode: str
    time: float  
    status: str 
    outcome: str 

