from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import argparse
import libtmux


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class StartCommand(Command):
    def __init__(self, receiver: Receiver, repos: List[str]) -> None:
        self._receiver = receiver
        self.repos = repos

    def execute(self) -> None:
        print(
            "StartCommand: Complex stuff should be done by a receiver object", end="\n"
        )
        # self._receiver.do_something(self._a)
        # self._receiver.do_something_else(self._b)
        self._receiver.launch_workspace_setup()
        print(args.repo, end="-----------------------------\n")


class Receiver:
    def do_something(self, a: str) -> None:
        print(f"\nReceiver: Working on ({a}.)", end="")

    def do_something_else(self, b: str) -> None:
        print(f"\nReceiver: Also working on ({b}.)", end="")

    def launch_workspace_setup(self) -> None:
        server = libtmux.Server()
        session = server.new_session(session_name="session_name", kill_session=True, attach=False)
        window = session.new_window(attach=False, window_name="window_name")
        pane1 = window.attached_pane
        pane2 = window.split_window(vertical=False)
        window.select_layout('tiled')
        pane1.send_keys('ls -al')
        pane2.send_keys('ls -al')
        server.attach_session(target_session="session_name")



class Invoker:
    def __init__(self) -> None:
        self._on_start = None
        self._progress = None
        self._on_finish = None

    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command) -> None:
        self._on_finish = command

    def do_something_important(self, command: Command) -> None:
        self._progress = command

        print("Invoker: Does anybody want something done before I begin?")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("Invoker: ...doing something really important...")
        self._progress.execute()

        print("Invoker: Does anybody want something done after I finish?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PROG")
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="sub-command help")
    parser_a = subparsers.add_parser("start", help="start help")
    parser_a.add_argument('-r', '--repo', type=str, nargs='*', required=True, help='repo help')
    args = parser.parse_args()

    invoker = Invoker()
    receiver = Receiver()

    invoker.do_something_important(StartCommand(receiver, args.repo))
