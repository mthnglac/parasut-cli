from __future__ import annotations
from ..lib.command import Command
from ..lib.receiver import Receiver


class Start(Command):
    def __init__(self, receiver: Receiver, a: str, b: str) -> None:
        self._receiver = receiver
        self._a = a
        self._b = b

    def execute(self) -> None:
        print(
            "LaunchWorkspace: Complex stuff should be done by a receiver object", end=""
        )
        self._receiver.do_something(self._a)
        self._receiver.do_something_else(self._b)
