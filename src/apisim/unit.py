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

@dataclass
class auth_request_unit:
    payload: dict 


@dataclass 
class token_unit:
    token: str
    url: str
