from dataclasses import dataclass
from typing import Any, Optional, List
import pydantic


@dataclass
class auth_request_unit:
    payload: dict


@dataclass
class token_unit:
    token: str
    url: str


@dataclass
class request_unit:
    url: list
    mode: str
    auth: str = None
    token: str = None


@dataclass
class response_unit:
    url: str
    value: str
    mode: str
    time: float
    status: str
    outcome: str
