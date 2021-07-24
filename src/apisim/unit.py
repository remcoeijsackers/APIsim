from dataclasses import dataclass
from typing import Any, Optional, List
from pydantic import BaseModel

@dataclass
class auth_request_unit:
    payload: dict 


@dataclass 
class token_unit:
    token: str
    url: str

@dataclass
class request_unit(BaseModel):
    url: str
    mode: str
    auth: Optional[auth_request_unit]
    token: Optional[token_unit]

@dataclass 
class response_unit:
    url: str
    value: str
    mode: str
    time: float  
    status: str 
    outcome: str 

