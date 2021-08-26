from __future__ import annotations
from typing import Optional

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class SwitchCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        show_output: bool,
        target_repo: Optional[str] = None,
        target_addling: Optional[str] = None,
        target_pricing_list: Optional[str] = None,
    ) -> None:
        self._receiver: Receiver = receiver
        self._target_repo: Optional[str] = target_repo
        self._target_addling: Optional[str] = target_addling
        self._target_pricing_list: Optional[str] = target_pricing_list
        self._show_output: bool = show_output

    def execute(self) -> None:
        if self._target_repo:
            self._receiver.switch_server_rails_frontend(
                target_repo=self._target_repo, show_output=self._show_output
            )
        if self._target_addling:
            self._receiver.switch_server_rails_addling(
                target_addling=self._target_addling, show_output=self._show_output
            )
        if self._target_pricing_list:
            self._receiver.switch_billing_rails_pricing_list(
                target_pricing_list=self._target_pricing_list, show_output=self._show_output
            )
