from __future__ import annotations
from typing import Dict, List
from libtmux import Server, Session, Window, Pane
from dotenv import dotenv_values
import os
import json
import subprocess

config = dotenv_values(".env")


class Receiver:
    def __init__(self):
        self._tmux_server: Server
        self._tmux_session_parasut_ws_setup: Session
        self._tmux_session_parasut_ws_editor: Session
        self._server_commands: Dict[str, str] = dict(
            launch_nvim="nvim",
            choose_ruby_version=f"rvm use {config['SERVER_RUBY_V']}",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails="rails server",
        )
        self._billing_commands = dict(
            launch_nvim="nvim",
            choose_ruby_version=f"rvm use {config['BILLING_RUBY_V']}",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails=f"rails server -p {config['BILLING_RAILS_PORT']}",
        )
        self._e_doc_broker_commands = dict(
            launch_nvim="nvim",
            choose_ruby_version=f"rvm use {config['E_DOC_BROKER_RUBY_V']}",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails=f"rails server -p {config['E_DOC_BROKER_RAILS_PORT']}",
        )
        self._phoenix_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version=f"yvm use {config['PHOENIX_YARN_V']}",
            choose_node_version=f"nvm use {config['PHOENIX_NODE_V']}",
            ember_serve="PROJECT_TARGET=phoenix ember s",
        )
        self._client_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version=f"yvm use {config['CLIENT_YARN_V']}",
            choose_node_version=f"nvm use {config['CLIENT_NODE_V']}",
            ember_serve=f"./node_modules/ember-cli/bin/ember s --live-reload-port {config['CLIENT_EMBER_PORT']}",
        )
        self._trinity_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version=f"yvm use {config['TRINITY_YARN_V']}",
            choose_node_version=f"nvm use {config['TRINITY_NODE_V']}",
            ember_serve="ember s --live-reload-port 6505",
        )
        self._ui_library_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version=f"yvm use {config['UI_LIBRARY_YARN_V']}",
            choose_node_version=f"nvm use {config['UI_LIBRARY_NODE_V']}",
            ember_serve=f"PROJECT_TARGET=phoenix ember s --live-reload-port {config['UI_LIBRARY_EMBER_PORT']}",
        )
        self._shared_logic_commands = dict(
            launch_nvim="nvim",
            choose_yarn_version=f"yvm use {config['SHARED_LOGIC_YARN_V']}",
            choose_node_version=f"nvm use {config['SHARED_LOGIC_NODE_V']}",
            ember_serve=f"ember s --live-reload-port {config['SHARED_LOGIC_EMBER_PORT']}",
        )

    def initialize_tmux_server(self) -> None:
        self._tmux_server = Server()

    def change_directory(self, path: str) -> None:
        os.chdir(os.path.expanduser(path))

    def apply_package_changes(self, force=False) -> None:
        subprocess.run(
            ["/bin/zsh", "-i", "-c", f'yarn install{" --force" if force else ""}']
        )

    def change_dependency_value(
        self, json_file_path: str, dep_key: str, dep_value: str
    ) -> str:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            dep_ver = data["devDependencies"][dep_key]
            data["devDependencies"][dep_key] = dep_value

        with open(json_file_path, "w+") as json_file:
            json_file.write(json.dumps(data, indent=True))
            json_file.close()

        return dep_ver

    def find_repo_path(self, repo_name: str) -> str:
        if "server" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['SERVER_DIR']}"
        elif "billing" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['BILLING_DIR']}"
        elif "e-doc-broker" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['E_DOC_BROKER_DIR']}"
        elif "client" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['CLIENT_DIR']}"
        elif "phoenix" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['PHOENIX_DIR']}"
        elif "shared-logic" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
        elif "trinity" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['TRINITY_DIR']}"
        elif "ui-library" in repo_name:
            return f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
        else:
            raise Exception(
                "Exiting because of an error: wrong repo path. couldn't find the repo"
            )

    def do_linking(self, base_repo: str, target_repos: List[str]) -> Dict[str, str]:
        base_path: str = self.find_repo_path(base_repo)

        dep_versions: Dict[str, str] = dict(ui_library="", shared_logic="")

        for repo_name in target_repos:
            if "ui-library" in repo_name:
                dep_key = "ui-library"
                dep_value = f"link:../{repo_name}"
                repo_path = f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
                json_file_path = f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}/package.json"

                dep_versions["ui-library"] = self.change_dependency_value(
                    json_file_path=json_file_path, dep_key=dep_key, dep_value=dep_value
                )
                self.apply_package_changes()
                self.change_directory(repo_path)
                self.apply_package_changes(force=True)
                self.change_directory(base_path)
            elif "shared_logic" in repo_name:
                dep_key = "shared-logic"
                dep_value = f"link:../{repo_name}"
                repo_path = f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
                json_file_path = f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}/package.json"

                dep_versions["shared-logic"] = self.change_dependency_value(
                    json_file_path=json_file_path, dep_key=dep_key, dep_value=dep_value
                )
                self.apply_package_changes()
                self.change_directory(repo_path)
                self.apply_package_changes(force=True)
                self.change_directory(base_path)

        return dep_versions

    def undo_linking(
        self, base_repo: str, repos: List[str], dep_versions: Dict[str, str]
    ) -> None:
        base_path: str = self.find_repo_path(base_repo)

        for repo_name in repos:
            if "ui-library" in repo_name:
                dep_key = "ui-library"
                dep_value = dep_versions["ui_library"]
                repo_path = f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
                json_file_path = f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}/package.json"

                self.change_dependency_value(
                    json_file_path=json_file_path, dep_key=dep_key, dep_value=dep_value
                )
                self.apply_package_changes()
                self.change_directory(repo_path)
                self.apply_package_changes(force=True)
                self.change_directory(base_path)
            elif "shared_logic" in repo_name:
                dep_key = "shared-logic"
                dep_value = dep_versions["shared_logic"]
                repo_path = f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
                json_file_path = f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}/package.json"

                self.change_dependency_value(
                    json_file_path=json_file_path, dep_key=dep_key, dep_value=dep_value
                )
                self.apply_package_changes()
                self.change_directory(repo_path)
                self.apply_package_changes(force=True)
                self.change_directory(base_path)

    def create_parasut_ws_setup(self, repos: List[str]) -> None:
        # create session
        self._tmux_session_parasut_ws_setup = self._tmux_server.new_session(
            session_name="parasut-ws-setup", kill_session=True, attach=False
        )
        # launch relative repos
        for repo_name in repos:
            if "server" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['SERVER_DIR']}"
                )
                self.launch_parasut_server_repo()
            elif "billing" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['BILLING_DIR']}"
                )
                self.launch_parasut_billing_repo()
            elif "e-doc-broker" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['E_DOC_BROKER_DIR']}"
                )
                self.launch_parasut_e_doc_broker_repo()
            elif "phoenix" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['PHOENIX_DIR']}"
                )
                self.launch_parasut_phoenix_repo()
            elif "client" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['CLIENT_DIR']}"
                )
                self.launch_parasut_client_repo()
            elif "trinity" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['TRINITY_DIR']}"
                )
                self.launch_parasut_trinity_repo()
            elif "ui-library" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
                )
                self.launch_parasut_ui_library_repo()
            elif "shared-logic" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
                )
                self.launch_parasut_shared_logic_repo()

        # kill the first empty window
        self._tmux_session_parasut_ws_setup.select_window(1).kill_window()

    def create_parasut_ws_editor(self, repos: List[str]) -> None:
        # create session
        self._tmux_session_parasut_ws_editor = self._tmux_server.new_session(
            session_name="parasut-ws-editor", kill_session=True, attach=False
        )
        # launch relative repos
        for repo_name in repos:
            if "server" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['SERVER_DIR']}"
                )
                self.launch_parasut_server_editor()
            elif "billing" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['BILLING_DIR']}"
                )
                self.launch_parasut_billing_editor()
            elif "e-doc-broker" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['E_DOC_BROKER_DIR']}"
                )
                self.launch_parasut_e_doc_broker_editor()
            elif "phoenix" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['PHOENIX_DIR']}"
                )
                self.launch_parasut_phoenix_editor()
            elif "client" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['CLIENT_DIR']}"
                )
                self.launch_parasut_client_editor()
            elif "trinity" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['TRINITY_DIR']}"
                )
                self.launch_parasut_trinity_editor()
            elif "ui-library" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
                )
                self.launch_parasut_ui_library_editor()
            elif "shared-logic" == repo_name:
                self.change_directory(
                    f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
                )
                self.launch_parasut_shared_logic_editor()
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
        server_pane.send_keys(
            " && ".join(
                [
                    self._server_commands["choose_ruby_version"],
                    self._server_commands["launch_rails"],
                ]
            )
        )
        server_sidekiq_pane.send_keys(
            " && ".join(
                [
                    self._server_commands["choose_ruby_version"],
                    self._server_commands["launch_sidekiq"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_server_editor(self) -> None:
        server_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="server"
        )
        server_pane: Pane = server_window.attached_pane

        server_pane.send_keys(
            " && ".join(
                [
                    self._server_commands["launch_nvim"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_billing_repo(self) -> None:
        billing_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="billing"
        )
        billing_pane: Pane = billing_window.attached_pane
        billing_sidekiq_pane: Pane = billing_window.split_window(vertical=False)

        billing_window.select_layout("tiled")
        # panes
        billing_pane.send_keys(
            " && ".join(
                [
                    self._billing_commands["choose_ruby_version"],
                    self._billing_commands["launch_rails"],
                ]
            )
        )
        billing_sidekiq_pane.send_keys(
            " && ".join(
                [
                    self._billing_commands["choose_ruby_version"],
                    self._billing_commands["launch_sidekiq"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_billing_editor(self) -> None:
        billing_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="billing"
        )
        billing_pane: Pane = billing_window.attached_pane

        billing_pane.send_keys(
            " && ".join(
                [
                    self._billing_commands["launch_nvim"],
                ]
            )
        )
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
        e_doc_broker_pane.send_keys(
            " && ".join(
                [
                    self._e_doc_broker_commands["choose_ruby_version"],
                    self._e_doc_broker_commands["launch_rails"],
                ]
            )
        )
        e_doc_broker_sidekiq_pane.send_keys(
            " && ".join(
                [
                    self._e_doc_broker_commands["choose_ruby_version"],
                    self._e_doc_broker_commands["launch_sidekiq"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_e_doc_broker_editor(self) -> None:
        e_doc_broker_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="e_doc_broker"
        )
        e_doc_broker_pane: Pane = e_doc_broker_window.attached_pane

        e_doc_broker_pane.send_keys(
            " && ".join(
                [
                    self._e_doc_broker_commands["launch_nvim"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_phoenix_repo(self) -> None:
        phoenix_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="phoenix"
        )
        phoenix_pane: Pane = phoenix_window.attached_pane

        phoenix_pane.send_keys(
            " && ".join(
                [
                    self._phoenix_commands["choose_yarn_version"],
                    self._phoenix_commands["choose_node_version"],
                    self._phoenix_commands["ember_serve"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_phoenix_editor(self) -> None:
        phoenix_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="phoenix"
        )
        phoenix_pane: Pane = phoenix_window.attached_pane

        phoenix_pane.send_keys(
            " && ".join(
                [
                    self._phoenix_commands["launch_nvim"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_client_repo(self) -> None:
        client_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="client"
        )
        client_pane: Pane = client_window.attached_pane

        client_pane.send_keys(
            " && ".join(
                [
                    self._client_commands["choose_yarn_version"],
                    self._client_commands["choose_node_version"],
                    self._client_commands["ember_serve"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_client_editor(self) -> None:
        client_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="client"
        )
        client_pane: Pane = client_window.attached_pane

        client_pane.send_keys(
            " && ".join(
                [
                    self._client_commands["launch_nvim"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_trinity_repo(self) -> None:
        trinity_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="trinity"
        )
        trinity_pane: Pane = trinity_window.attached_pane

        trinity_pane.send_keys(
            " && ".join(
                [
                    self._trinity_commands["choose_yarn_version"],
                    self._trinity_commands["choose_node_version"],
                    self._trinity_commands["ember_serve"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_trinity_editor(self) -> None:
        trinity_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="trinity"
        )
        trinity_pane: Pane = trinity_window.attached_pane

        trinity_pane.send_keys(
            " && ".join(
                [
                    self._trinity_commands["launch_nvim"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_ui_library_repo(self) -> None:
        ui_library_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="ui_library"
        )
        ui_library_pane: Pane = ui_library_window.attached_pane

        ui_library_pane.send_keys(
            " && ".join(
                [
                    self._ui_library_commands["choose_yarn_version"],
                    self._ui_library_commands["choose_node_version"],
                    self._ui_library_commands["ember_serve"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_ui_library_editor(self) -> None:
        ui_library_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="ui_library"
        )
        ui_library_pane: Pane = ui_library_window.attached_pane

        ui_library_pane.send_keys(
            " && ".join(
                [
                    self._ui_library_commands["launch_nvim"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_shared_logic_repo(self) -> None:
        shared_logic_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="shared_logic"
        )
        shared_logic_pane: Pane = shared_logic_window.attached_pane

        shared_logic_pane.send_keys(
            " && ".join(
                [
                    self._shared_logic_commands["choose_yarn_version"],
                    self._shared_logic_commands["choose_node_version"],
                    self._shared_logic_commands["ember_serve"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")

    def launch_parasut_shared_logic_editor(self) -> None:
        shared_logic_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="shared_logic"
        )
        shared_logic_pane: Pane = shared_logic_window.attached_pane

        shared_logic_pane.send_keys(
            " && ".join(
                [
                    self._shared_logic_commands["launch_nvim"],
                ]
            )
        )
        # server.attach_session(target_session="session_name")
