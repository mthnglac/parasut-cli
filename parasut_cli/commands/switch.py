from __future__ import annotations
from typing import List, Dict, Optional

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class SwitchCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        target_repo: Optional[str] = None,
        target_addling: Optional[str] = None,
    ) -> None:
        self._receiver: Receiver = receiver
        self._target_repo: Optional[str] = target_repo
        self._target_addling: Optional[str] = target_addling

    def execute(self) -> None:
        if self._target_repo:
            self._receiver.switch_server_rails_frontend(self._target_repo)
        if self._target_addling:
            self._receiver.switch_server_rails_addling(self._target_addling)
