from __future__ import annotations
from typing import List

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class LinkCommand(Command):
    def __init__(self, receiver: Receiver, repos: List[str]) -> None:
        self._receiver: Receiver = receiver
        self._repos: List[str] = repos

    def execute(self) -> None:
        for repo in self._repos:
            self._receiver.change_package_value(repo)
            self._receiver.apply_package_changes()
            # ??? burda mi yoklasak methodun icinde mi?
            # emin olamadim?
            self._receiver.change_directory(repo=repo)
            self._receiver.apply_package_changes(force=True)
            self._receiver.change_directory(path=env.CURRENT_PROJECT_PATH)
