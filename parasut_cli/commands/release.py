from __future__ import annotations

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class ReleaseCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        target_repo: str,
    ) -> None:
        self._receiver: Receiver = receiver
        self._target_repo: str = target_repo

    def execute(self) -> None:
        if self._target_repo:
            self._receiver.release_repo(target_repo=self._target_repo)
