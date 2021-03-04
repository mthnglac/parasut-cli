from __future__ import annotations
from typing import Dict, List, Optional
from libtmux import Server, Session, Window, Pane
from dotenv import dotenv_values
import os
import json
import subprocess
import pickle

config = {
    **dotenv_values(".envs/.env.shared"),
    **dotenv_values(".envs/.env.secret"),
}


class Receiver:
    def __init__(self):
        self._tmux_server: Server
        self._tmux_session_parasut_ws_setup: Session
        self._tmux_session_parasut_ws_editor: Session
        self._dep_versions = dict(
            ui_library=dict(linked=False, value=""),
            shared_logic=dict(linked=False, value=""),
        )
        self._linking_options = dict(
            ui_library="ui-library",
            shared_logic="shared-logic",
        )
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
        attempts = 0

        while attempts < 3:
            try:
                subprocess.run(
                    ["/bin/zsh", "-c", f'yarn install{" --force" if force else ""}'],
                    check=True,
                )
                break
            except subprocess.CalledProcessError:
                attempts += 1

    def change_dependency_value(
        self, dep_json_file: str, dep_key: str, dep_value: str
    ) -> str:
        with open(dep_json_file, "r") as json_file:
            data = json.load(json_file)
            dep_ver = data["devDependencies"][dep_key]
            data["devDependencies"][dep_key] = dep_value

        with open(dep_json_file, "w+") as json_file:
            json_file.write(json.dumps(data, indent=True))
            json_file.close()

        return dep_ver

    def switch_server_rails(self, target_repo: str) -> None:
        server_repo = f"{config['PARASUT_BASE_DIR']}/{config['SERVER_DIR']}"

        self.change_directory(server_repo)

        # shut up! this telescope is necessary.
        # don't judge me, judge rvm.
        if target_repo == "phoenix":
            subprocess.run(
                [
                    "/bin/zsh",
                    "-i",
                    "-c",
                    f"rvm use {config['SERVER_RUBY_V']} && rails runner 'puts Company.find({config['COMPANY_ID']}).update!(used_app: \"{config['PHOENIX_SWITCH_NAME']}\")'",
                ]
            )
        if target_repo == "trinity":
            subprocess.run(
                [
                    "/bin/zsh",
                    "-i",
                    "-c",
                    f"rvm use {config['SERVER_RUBY_V']} && rails runner 'puts Company.find({config['COMPANY_ID']}).update!(used_app: \"{config['TRINITY_SWITCH_NAME']}\")'",
                ]
            )

    def get_project_root_dir(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def find_repo_path(self, repo_name: str) -> str:
        if repo_name == "server":
            return f"{config['PARASUT_BASE_DIR']}/{config['SERVER_DIR']}"
        elif repo_name == "billing":
            return f"{config['PARASUT_BASE_DIR']}/{config['BILLING_DIR']}"
        elif repo_name == "e-doc-broker":
            return f"{config['PARASUT_BASE_DIR']}/{config['E_DOC_BROKER_DIR']}"
        elif repo_name == "client":
            return f"{config['PARASUT_BASE_DIR']}/{config['CLIENT_DIR']}"
        elif repo_name == "phoenix":
            return f"{config['PARASUT_BASE_DIR']}/{config['PHOENIX_DIR']}"
        elif repo_name == "shared-logic":
            return f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
        elif repo_name == "trinity":
            return f"{config['PARASUT_BASE_DIR']}/{config['TRINITY_DIR']}"
        elif repo_name == "ui-library":
            return f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
        else:
            raise Exception(
                "Exiting because of an error: wrong repo path. couldn't find the repo"
            )

    def store_linking_info(self, dep_versions: Dict) -> None:
        cli_root_path = self.get_project_root_dir()
        pickle_file_path = f"{cli_root_path}/state/link_info.pickle"

        with open(pickle_file_path, "wb") as handle:
            pickle.dump(dep_versions, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def initialize_dep_versions(self, base_repo: str) -> None:
        root_path = self.get_project_root_dir()
        pickle_file_path = f"{root_path}/state/link_info.pickle"

        try:
            with open(pickle_file_path, "rb") as handle:
                self._dep_versions = pickle.load(handle)
        except FileNotFoundError:
            with open(pickle_file_path, "wb") as handle:
                pickle.dump(
                    self._dep_versions, handle, protocol=pickle.HIGHEST_PROTOCOL
                )

        for i, j in self._linking_options.items():
            if self.is_linked(base_repo=base_repo, dep_key=j):
                self._dep_versions[i]["linked"] = True
            else:
                self._dep_versions[i]["linked"] = False

    def do_linking(self, base_repo: str, target_repos: List[str]) -> None:
        base_path: str = self.find_repo_path(base_repo)

        self.initialize_dep_versions(base_repo)
        self.change_directory(base_path)

        for repo_name in target_repos:
            if repo_name == "ui-library":
                dep_key = "ui-library"
                dep_value = f"link:../{repo_name}"
                target_path = f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
                json_file = "package.json"

                if self._dep_versions["ui_library"]["linked"] == True:
                    print(
                        f"{repo_name} has been linked before. Try --list to check linked repos."
                    )
                else:
                    self._dep_versions["ui_library"][
                        "value"
                    ] = self.change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["ui_library"]["linked"] = True

                    self.store_linking_info(self._dep_versions)
                    self.apply_package_changes()
                    self.change_directory(target_path)
                    self.apply_package_changes(force=True)
                    self.change_directory(base_path)
            elif repo_name == "shared-logic":
                dep_key = "shared-logic"
                dep_value = f"link:../{repo_name}"
                target_path = (
                    f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
                )
                json_file = "package.json"

                if self._dep_versions["shared_logic"]["linked"] == True:
                    print(
                        f"{repo_name} has been linked before. Try --list to check linked repos."
                    )
                else:
                    self._dep_versions["shared_logic"][
                        "value"
                    ] = self.change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["shared_logic"]["linked"] = True

                    self.store_linking_info(self._dep_versions)
                    self.apply_package_changes()
                    self.change_directory(target_path)
                    self.apply_package_changes(force=True)
                    self.change_directory(base_path)

    def undo_linking(self, base_repo: str, repos: List[str]) -> None:
        base_path: str = self.find_repo_path(base_repo)

        self.initialize_dep_versions(base_repo)
        self.change_directory(base_path)

        for repo_name in repos:
            if repo_name == "ui-library":
                dep_key = "ui-library"
                dep_value = self._dep_versions["ui_library"]["value"]
                target_path = f"{config['PARASUT_BASE_DIR']}/{config['UI_LIBRARY_DIR']}"
                json_file = "package.json"

                if self._dep_versions["ui_library"]["linked"] == False:
                    print(
                        f"{repo_name} has not been linked before. Try listing linked repos."
                    )
                else:
                    self.change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["ui_library"]["linked"] = False

                    self.apply_package_changes()
                    self.change_directory(target_path)
                    self.apply_package_changes(force=True)
                    self.change_directory(base_path)
            elif repo_name == "shared-logic":
                dep_key = "shared-logic"
                dep_value = self._dep_versions["shared_logic"]["value"]
                target_path = (
                    f"{config['PARASUT_BASE_DIR']}/{config['SHARED_LOGIC_DIR']}"
                )
                json_file = "package.json"

                if self._dep_versions["shared_logic"]["linked"] == False:
                    print(
                        f"{repo_name} has not been linked before. Try listing linked repos."
                    )
                else:
                    self.change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["shared_logic"]["linked"] = False

                    self.apply_package_changes()
                    self.change_directory(target_path)
                    self.apply_package_changes(force=True)
                    self.change_directory(base_path)

    def get_linked_repos(self, base_repo: str) -> None:
        for key, value in self._dep_versions.items():
            if self._dep_versions[key]["linked"]:
                print(key)
        else:
            print("There is no repo linked by this cli.")

    def is_linked(self, base_repo: str, dep_key: str):
        base_path: str = self.find_repo_path(base_repo)
        checking_word = "link"
        json_file = "package.json"

        self.change_directory(base_path)

        with open(json_file, "r") as file:
            data = json.load(file)
            if checking_word in data["devDependencies"][dep_key]:
                return True
            else:
                return False

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
