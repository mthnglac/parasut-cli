from __future__ import annotations

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class ReleaseCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        target_repo: str,
        auto_login: bool,
        show_output: bool,
    ) -> None:
        self._receiver: Receiver = receiver
        self._target_repo: str = target_repo
        self._auto_login: bool = auto_login
        self._show_output: bool = show_output

    def execute(self) -> None:
        if self._target_repo:
            self._receiver.release_repo(
                target_repo=self._target_repo,
                show_output=self._show_output,
                auto_login=self._auto_login,
            )
