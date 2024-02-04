from __future__ import annotations

from typing import Any
from abc import ABC, abstractclassmethod

class SerialABC(ABC):
    @abstractclassmethod
    def from_json(cls, *args, **kwargs) -> SerialABC:
        ...
