"""
AuraBeats - Base Model
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from datetime import datetime
from typing import Any, Dict


class BaseModel:
    """Base class for all models"""

    def __init__(self, **kwargs):
        self._data: Dict[str, Any] = kwargs
        self._data.setdefault("created_at", datetime.utcnow().isoformat())
        self._data["updated_at"] = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dict"""
        return dict(self._data)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value
        self._data["updated_at"] = datetime.utcnow().isoformat()

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        return self._data.get(name)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._data}>"
