from __future__ import annotations
from typing import List, Dict, Optional

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command


class LinkCommand(Command):
    def __init__(
        self,
        receiver: Receiver,
        base_repo: str,
        target_repos: Optional[List[str]],
        undo_linked_repos: Optional[List[str]],
        list_linked_repos: Optional[bool],
    ) -> None:
        self._receiver: Receiver = receiver
        self._base_repo: str = base_repo
        self._target_repos: Optional[List[str]] = target_repos
        self._undo_linked_repos: Optional[List[str]] = undo_linked_repos
        self._list_linked_repos: Optional[bool] = list_linked_repos

    def execute(self) -> None:
        if self._target_repos:
            self._receiver.do_linking(self._base_repo, self._target_repos)
        if self._undo_linked_repos:
            self._receiver.undo_linking(self._base_repo, self._undo_linked_repos)
        if self._list_linked_repos:
            self._receiver.get_linked_repos(self._base_repo)
