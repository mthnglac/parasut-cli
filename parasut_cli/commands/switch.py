from __future__ import annotations
from typing import List, Dict, Optional

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class SwitchCommand(Command):
    def __init__(self, receiver: Receiver, target_repo: str) -> None:
        self._receiver: Receiver = receiver
        self._target_repo: str = target_repo

    def execute(self) -> None:
        self._receiver.switch_server_rails(self._target_repo)
