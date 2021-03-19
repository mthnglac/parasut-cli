from __future__ import annotations

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class RunCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        repo_name: str,
    ) -> None:
        self._receiver: Receiver = receiver
        self._repo_name: str = repo_name

    def execute(self) -> None:
        if self._repo_name:
            self._receiver.run_repo(repo_name=self._repo_name)
