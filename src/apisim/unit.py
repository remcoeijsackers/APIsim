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
    auth: dict = None
    token: str = None
    auth_url: str = None


@dataclass
class response_unit:
    url: str
    value: str
    mode: str
    time: float
    status: str
    outcome: str

@dataclass
class config_unit:
    auto_printsteps: bool
    auto_fallback: bool
    auto_printtable: bool
    count_repeat: int