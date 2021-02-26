from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import argparse
from libtmux import Server, Session, Window, Pane


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class StartCommand(Command):
    def __init__(self, receiver: Receiver, repos: List[str]) -> None:
        self._receiver = receiver
        self.repos = repos

    def execute(self) -> None:
        self._receiver.initialize_tmux_server()
        self._receiver.create_parasut_ws_setup()

        self._receiver.launch_parasut_server_repo()
        self._receiver.launch_parasut_billing_repo()
        self._receiver.launch_parasut_e_doc_broker_repo()
        self._receiver.launch_parasut_phoenix_repo()
        self._receiver.launch_parasut_client_repo()
        self._receiver.launch_parasut_trinity_repo()
        self._receiver.launch_parasut_ui_library_repo()
        print(args.repo, end="-----------------------------\n")


class Receiver:
    def __init__(self) -> None:
        self.tmux_server: Server
        self.tmux_session_parasut_ws_setup: Session
        self.tmux_session_parasut_ws_editor: Session

    def reset(self) -> None:
        self.tmux_server = None
        self.tmux_session_parasut_ws_setup = None
        self.tmux_session_parasut_ws_editor = None

    def initialize_tmux_server(self) -> None:
        self.tmux_server = Server()

    def create_parasut_ws_setup(self) -> None:
        self.tmux_session_parasut_ws_setup = self.tmux_server.new_session(session_name="parasut-ws-setup", kill_session=True, attach=False)

    def launch_parasut_server_repo(self) -> None:
        server_window: Window = self.tmux_session_parasut_ws_setup.new_window(attach=False, window_name="server")
        server_pane: Pane = server_window.attached_pane
        server_sidekiq_pane: Pane = server_window.split_window(vertical=False)

        server_window.select_layout("tiled")
        # panes
        server_pane.send_keys("echo 'server'")
        server_sidekiq_pane.send_keys("echo 'server sidekiq'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_billing_repo(self) -> None:
        billing_window: Window = self.tmux_session_parasut_ws_setup.new_window(attach=False, window_name="billing")
        billing_pane: Pane = billing_window.attached_pane
        billing_sidekiq_pane: Pane = billing_window.split_window(vertical=False)

        billing_window.select_layout("tiled")
        # panes
        billing_pane.send_keys("echo 'billing'")
        billing_sidekiq_pane.send_keys("echo 'billing sidekiq'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_e_doc_broker_repo(self) -> None:
        e_doc_broker_window: Window = self.tmux_session_parasut_ws_setup.new_window(attach=False, window_name="e_doc_broker")
        e_doc_broker_pane: Pane = e_doc_broker_window.attached_pane
        e_doc_broker_sidekiq_pane: Pane = e_doc_broker_window.split_window(vertical=False)

        e_doc_broker_window.select_layout("tiled")
        # panes
        e_doc_broker_pane.send_keys("echo 'e_doc_broker'")
        e_doc_broker_sidekiq_pane.send_keys("echo 'e_doc_broker sidekiq'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_phoenix_repo(self) -> None:
        phoenix_window: Window = self.tmux_session_parasut_ws_setup.new_window(attach=False, window_name="phoenix")
        phoenix_pane: Pane = phoenix_window.attached_pane

        phoenix_pane.send_keys("echo 'phoenix'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_client_repo(self) -> None:
        client_window: Window = self.tmux_session_parasut_ws_setup.new_window(attach=False, window_name="client")
        client_pane: Pane = client_window.attached_pane

        client_pane.send_keys("echo 'client'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_trinity_repo(self) -> None:
        trinity_window: Window = self.tmux_session_parasut_ws_setup.new_window(attach=False, window_name="trinity")
        trinity_pane: Pane = trinity_window.attached_pane

        trinity_pane.send_keys("echo 'trinity'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_ui_library_repo(self) -> None:
        ui_library_window: Window = self.tmux_session_parasut_ws_setup.new_window(attach=False, window_name="ui_library")
        ui_library_pane: Pane = ui_library_window.attached_pane

        ui_library_pane.send_keys("echo 'ui_library'")
        # server.attach_session(target_session="session_name")


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
