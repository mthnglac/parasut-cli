from __future__ import annotations
from datetime import datetime

from parasut_cli.utils.state.memento import Memento


class ConcreteMemento(Memento):
    def __init__(self, state: str) -> None:
        self._state: str = state
        self._date: str = str(datetime.now())[:19]

    def get_state(self) -> str:
        return self._state

    def get_name(self) -> str:
        return f"{self._date} / ({self._state[0:9]}...)"

    def get_date(self) -> str:
        return self._date
