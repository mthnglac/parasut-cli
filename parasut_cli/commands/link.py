from __future__ import annotations
from typing import List, Optional

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class LinkCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        base_repo: str,
        target_repos: Optional[List[str]],
        undo_linked_repos: Optional[List[str]],
        list_linked_repos: bool,
        show_output: bool,
    ) -> None:
        self._receiver: Receiver = receiver
        self._base_repo: str = base_repo
        self._target_repos: Optional[List[str]] = target_repos
        self._undo_linked_repos: Optional[List[str]] = undo_linked_repos
        self._list_linked_repos: bool = list_linked_repos
        self._show_output: bool = show_output

    def execute(self) -> None:
        if self._target_repos:
            self._receiver.do_linking(
                self._base_repo, self._target_repos, show_output=self._show_output
            )
        if self._undo_linked_repos:
            self._receiver.undo_linking(
                self._base_repo, self._undo_linked_repos, show_output=self._show_output
            )
        if self._list_linked_repos:
            self._receiver.get_linked_repos(self._base_repo)
