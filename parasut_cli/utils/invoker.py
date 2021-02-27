from __future__ import annotations
from libtmux import Server, Session, Window, Pane
import argparse

from parasut_cli.utils.command import Command


class Invoker:
    _on_start: Command
    _progress: Command
    _on_finish: Command

    def set_on_start(self, command: Command) -> None:
        self._on_start = command

    def set_on_finish(self, command: Command) -> None:
        self._on_finish = command

    def do_something_important(self, command: Command) -> None:
        self._progress = command

        # print("Invoker: Does anybody want something done before I begin?")
        # self._on_start.execute()

        print("Invoker: ...doing something really important...")
        self._progress.execute()

        # print("Invoker: Does anybody want something done after I finish?")
        # self._on_finish.execute()
