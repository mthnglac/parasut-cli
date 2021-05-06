from __future__ import annotations

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class VersionCommand(Command):
    def __init__(self, receiver: Receiver) -> None:
        self._receiver: Receiver = receiver

    def execute(self) -> None:
        self._receiver.get_pkg_version()
