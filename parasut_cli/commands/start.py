from __future__ import annotations
from typing import List, Optional

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class StartCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        setup_repos: Optional[List[str]],
        edit_repos: Optional[List[str]],
        workers: Optional[List[str]],
    ) -> None:
        self._receiver: Receiver = receiver
        self._setup_repos: Optional[List[str]] = setup_repos
        self._edit_repos: Optional[List[str]] = edit_repos
        self._workers: Optional[List[str]] = workers

    def execute(self) -> None:
        self._receiver.initialize_tmux_server()
        if self._setup_repos:
            self._receiver.create_parasut_ws_setup(self._setup_repos)
        if self._edit_repos:
            self._receiver.create_parasut_ws_editor(self._edit_repos)
        if self._workers:
            self._receiver.create_parasut_ws_worker(self._workers)
