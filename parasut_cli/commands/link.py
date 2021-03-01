from __future__ import annotations
from typing import List, Dict, Optional

from parasut_cli.utils.receiver import Receiver
from parasut_cli.utils.command import Command
from parasut_cli.utils.state.originator import Originator
from parasut_cli.utils.state.caretaker import Caretaker


class LinkCommand(Command):
    # _originator = Originator("Super-duper-super-puper-super.")
    # _caretaker = Caretaker(_originator)

    def __init__(
        self,
        receiver: Receiver,
        base_repo: str,
        target_repos: Optional[List[str]],
        undo_linked_repos: Optional[List[str]],
    ) -> None:
        self._receiver: Receiver = receiver
        self._base_repo: str = base_repo
        self._target_repos: Optional[List[str]] = target_repos
        self._undo_linked_repos: Optional[List[str]] = undo_linked_repos

    def execute(self) -> None:
        dep_versions: Dict[str, str] = dict(ui_library="", shared_logic="")

        # self._caretaker.backup()
        # self._originator.do_something()

        # self._caretaker.backup()
        # self._originator.do_something()

        # self._caretaker.backup()
        # self._originator.do_something()

        # print()
        # self._caretaker.show_history()

        # print("\nClient: Now, let's rollback!\n")
        # self._caretaker.undo()

        # print("\nClient: Once more!\n")
        # self._caretaker.undo()

        # print("\nClient: Once more!\n")
        # self._caretaker.undo()

        if self._target_repos:
            # dep_versions |= self._receiver.do_linking(self._base_repo, self._target_repos)
            print(self._base_repo)
            print(self._target_repos)
            print(self._undo_linked_repos)
        if self._undo_linked_repos:
            # self._receiver.undo_linking(self._base_repo, self._undo_linked_repos, dep_versions)
            print(self._base_repo)
            print(self._target_repos)
            print(self._undo_linked_repos)
