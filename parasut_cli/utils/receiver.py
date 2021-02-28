from __future__ import annotations
from typing import Dict
from libtmux import Server, Session, Window, Pane


class Receiver:
    def __init__(self):
        self._tmux_server: Server
        self._tmux_session_parasut_ws_setup: Session
        self._tmux_session_parasut_ws_editor: Session
        self._server_commands: Dict[str, str] = dict(
            launch_nvim="nvim",
            choose_ruby_version="rvm use 2.6.6",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails="rails server",
        )
        self._billing_commands = dict(
            launch_nvim="nvim",
            choose_ruby_version="rvm use 2.4.2",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails="rails server -p 4002",
        )
        self._e_doc_broker_commands = dict(
            launch_nvim="nvim",
            choose_ruby_version="rvm use 2.5.1",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails="rails server -p 5002",
        )
        self._phoenix_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version="yvm use 1.21.1",
            choose_node_version="nvm use 8.16.0",
            ember_serve="PROJECT_TARGET=phoenix ember s",
        )
        self._client_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version="yvm use 1.21.1",
            choose_node_version="nvm use 0.11.16",
            ember_serve="./node_modules/ember-cli/bin/ember s --live-reload-port 6500",
        )
        self._trinity_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version="yvm use 1.21.1",
            choose_node_version="nvm use 8.16.0",
            ember_serve="ember s --live-reload-port 6505",
        )
        self._ui_library_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version="yvm use 1.21.1",
            choose_node_version="nvm use 8.16.0",
            ember_serve="PROJECT_TARGET=phoenix ember s --live-reload-port 6510",
        )
        self._shared_logic_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version="yvm use 1.21.1",
            choose_node_version="nvm use 8.16.0",
            ember_serve="ember s --live-reload-port 6515",
        )

    def initialize_tmux_server(self) -> None:
        self._tmux_server = Server()

    def create_parasut_ws_setup(self) -> None:
        # create session
        self._tmux_session_parasut_ws_setup = self._tmux_server.new_session(
            session_name="parasut-ws-setup", kill_session=True, attach=False
        )
        # launch relative repos
        self.launch_parasut_server_repo()
        self.launch_parasut_billing_repo()
        self.launch_parasut_e_doc_broker_repo()
        self.launch_parasut_phoenix_repo()
        self.launch_parasut_client_repo()
        self.launch_parasut_trinity_repo()
        self.launch_parasut_ui_library_repo()
        # kill the first empty window
        self._tmux_session_parasut_ws_setup.select_window(1).kill_window()

    def create_parasut_ws_editor(self) -> None:
        # create session
        self._tmux_session_parasut_ws_editor = self._tmux_server.new_session(
            session_name="parasut-ws-editor", kill_session=True, attach=False
        )
        # launch relative repos
        self.launch_parasut_phoenix_editor()
        self.launch_parasut_shared_logic_editor()
        self.launch_parasut_client_editor()
        self.launch_parasut_trinity_editor()
        self.launch_parasut_ui_library_editor()
        # kill the first empty window
        self._tmux_session_parasut_ws_editor.select_window(1).kill_window()

    def launch_parasut_server_repo(self) -> None:
        server_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="server"
        )
        server_pane: Pane = server_window.attached_pane
        server_sidekiq_pane: Pane = server_window.split_window(vertical=False)

        server_window.select_layout("tiled")
        # panes
        server_pane.send_keys("echo 'server'")
        server_sidekiq_pane.send_keys("echo 'server sidekiq'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_billing_repo(self) -> None:
        billing_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="billing"
        )
        billing_pane: Pane = billing_window.attached_pane
        billing_sidekiq_pane: Pane = billing_window.split_window(vertical=False)

        billing_window.select_layout("tiled")
        # panes
        billing_pane.send_keys("echo 'billing'")
        billing_sidekiq_pane.send_keys("echo 'billing sidekiq'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_e_doc_broker_repo(self) -> None:
        e_doc_broker_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="e_doc_broker"
        )
        e_doc_broker_pane: Pane = e_doc_broker_window.attached_pane
        e_doc_broker_sidekiq_pane: Pane = e_doc_broker_window.split_window(
            vertical=False
        )

        e_doc_broker_window.select_layout("tiled")
        # panes
        e_doc_broker_pane.send_keys("echo 'e_doc_broker'")
        e_doc_broker_sidekiq_pane.send_keys("echo 'e_doc_broker sidekiq'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_phoenix_repo(self) -> None:
        phoenix_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="phoenix"
        )
        phoenix_pane: Pane = phoenix_window.attached_pane

        phoenix_pane.send_keys("echo 'phoenix'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_phoenix_editor(self) -> None:
        phoenix_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="phoenix"
        )
        phoenix_pane: Pane = phoenix_window.attached_pane

        phoenix_pane.send_keys("echo 'phoenix'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_client_repo(self) -> None:
        client_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="client"
        )
        client_pane: Pane = client_window.attached_pane

        client_pane.send_keys("echo 'client'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_client_editor(self) -> None:
        client_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="client"
        )
        client_pane: Pane = client_window.attached_pane

        client_pane.send_keys("echo 'client'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_trinity_repo(self) -> None:
        trinity_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="trinity"
        )
        trinity_pane: Pane = trinity_window.attached_pane

        trinity_pane.send_keys("echo 'trinity'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_trinity_editor(self) -> None:
        trinity_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="trinity"
        )
        trinity_pane: Pane = trinity_window.attached_pane

        trinity_pane.send_keys("echo 'trinity'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_ui_library_repo(self) -> None:
        ui_library_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="ui_library"
        )
        ui_library_pane: Pane = ui_library_window.attached_pane

        ui_library_pane.send_keys("echo 'ui_library'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_ui_library_editor(self) -> None:
        ui_library_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="ui_library"
        )
        ui_library_pane: Pane = ui_library_window.attached_pane

        ui_library_pane.send_keys("echo 'ui_library'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_shared_logic_repo(self) -> None:
        shared_logic_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="shared_logic"
        )
        shared_logic_pane: Pane = shared_logic_window.attached_pane

        shared_logic_pane.send_keys("echo 'shared_logic'")
        # server.attach_session(target_session="session_name")

    def launch_parasut_shared_logic_editor(self) -> None:
        shared_logic_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="shared_logic"
        )
        shared_logic_pane: Pane = shared_logic_window.attached_pane

        shared_logic_pane.send_keys("echo 'shared_logic'")
        # server.attach_session(target_session="session_name")
