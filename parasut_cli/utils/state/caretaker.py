from __future__ import annotations
from typing import List

from parasut_cli.utils.state.originator import Originator
from parasut_cli.utils.state.memento import Memento


class Caretaker():
    def __init__(self, originator: Originator) -> None:
        self._mementos: List[Memento] = []
        self._originator: Originator = originator

    def backup(self) -> None:
        print("\nCaretaker: Saving Originator's state...")
        self._mementos.append(self._originator.save())

    def undo(self) -> None:
        if not len(self._mementos):
            return

        memento: Memento = self._mementos.pop()
        print(f"Caretaker: Restoring state to: {memento.get_name()}")
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento.get_name())
