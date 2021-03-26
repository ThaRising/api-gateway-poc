from contextvars import ContextVar
from typing import Any

import peewee
from pydantic.utils import GetterDict

db_state_default = {
    "closed": None, "conn": None, "ctx": None, "transactions": None
}


class PeeweeConnectionState(peewee._ConnectionState):  # noqa
    def __init__(self, **kwargs):
        super().__setattr__(
            "_state", ContextVar("db_state", default=db_state_default.copy())
        )
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


def get_state_adapter(adapter):
    setattr(adapter, "_state", PeeweeConnectionState())
    return adapter


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


__all__ = [
    "get_state_adapter", "PeeweeConnectionState", "PeeweeGetterDict"
]
