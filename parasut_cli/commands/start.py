from __future__ import annotations
from typing import List

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class StartCommand(Command):
    def __init__(self, receiver: Receiver, repos: List[str]) -> None:
        self._receiver: Receiver = receiver
        self._repos: List[str] = repos

    def execute(self) -> None:
        self._receiver.initialize_tmux_server()
        self._receiver.create_parasut_ws_setup()
        self._receiver.create_parasut_ws_editor()

        print(self._repos, end="-----------------------------\n")
