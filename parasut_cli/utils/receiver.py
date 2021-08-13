from __future__ import annotations
from typing import Dict, List, Optional, Any
from time import sleep
from libtmux import Server, Session, Window, Pane
from libtmux.exc import LibTmuxException
from rich.console import Console
import os
import sys
import json
import subprocess
import pickle
import parasut_cli

from parasut_cli.config.settings import APP_DIR, env

console = Console()


class Receiver:
    def __init__(self) -> None:
        # env variables
        try:
            # core
            self.COMPANY_ID: str = env["PARASUT_COMPANY_ID"]
            self.PARASUT_REGISTRY: str = env["PARASUT_REGISTRY"]
            self.PARASUT_BASE_DIR: str = env["PARASUT_BASE_DIR"]
            self.PARASUT_CLI_TEXT_EDITOR: str = env["PARASUT_CLI_TEXT_EDITOR"]
            self.PARASUT_NPM_USERNAME: str = env["PARASUT_NPM_USERNAME"]
            self.PARASUT_NPM_PASSWORD: str = env["PARASUT_NPM_PASSWORD"]
            self.PARASUT_NPM_EMAIL: str = env["PARASUT_NPM_EMAIL"]
            # server
            self.SERVER_RUBY_V: str = env["PARASUT_SERVER_RUBY_V"]
            self.SERVER_DIR: str = env["PARASUT_SERVER_DIR"]
            # billing
            self.BILLING_RUBY_V: str = env["PARASUT_BILLING_RUBY_V"]
            self.BILLING_RAILS_PORT: str = env["PARASUT_BILLING_RAILS_PORT"]
            self.BILLING_DIR: str = env["PARASUT_BILLING_DIR"]
            # e-doc-broker
            self.E_DOC_BROKER_RUBY_V: str = env["PARASUT_E_DOC_BROKER_RUBY_V"]
            self.E_DOC_BROKER_RAILS_PORT: str = env["PARASUT_E_DOC_BROKER_RAILS_PORT"]
            self.E_DOC_BROKER_DIR: str = env["PARASUT_E_DOC_BROKER_DIR"]
            # post-office
            self.POST_OFFICE_RUBY_V: str = env["PARASUT_POST_OFFICE_RUBY_V"]
            self.POST_OFFICE_RAILS_PORT: str = env["PARASUT_POST_OFFICE_RAILS_PORT"]
            self.POST_OFFICE_DIR: str = env["PARASUT_POST_OFFICE_DIR"]
            # ubl-validator
            self.UBL_VALIDATOR_MAVEN_V: str = env["PARASUT_UBL_VALIDATOR_MAVEN_V"]
            self.UBL_VALIDATOR_DIR: str = env["PARASUT_UBL_VALIDATOR_DIR"]
            # phoenix
            self.PHOENIX_NODE_V: str = env["PARASUT_PHOENIX_NODE_V"]
            self.PHOENIX_YARN_V: str = env["PARASUT_PHOENIX_YARN_V"]
            self.PHOENIX_DIR: str = env["PARASUT_PHOENIX_DIR"]
            self.PHOENIX_SWITCH_NAME: str = env["PARASUT_PHOENIX_SWITCH_NAME"]
            # client
            self.CLIENT_NODE_V: str = env["PARASUT_CLIENT_NODE_V"]
            self.CLIENT_YARN_V: str = env["PARASUT_CLIENT_YARN_V"]
            self.CLIENT_EMBER_PORT: str = env["PARASUT_CLIENT_EMBER_PORT"]
            self.CLIENT_DIR: str = env["PARASUT_CLIENT_DIR"]
            # trinity
            self.TRINITY_NODE_V: str = env["PARASUT_TRINITY_NODE_V"]
            self.TRINITY_YARN_V: str = env["PARASUT_TRINITY_YARN_V"]
            self.TRINITY_EMBER_PORT: str = env["PARASUT_TRINITY_EMBER_PORT"]
            self.TRINITY_SWITCH_NAME: str = env["PARASUT_TRINITY_SWITCH_NAME"]
            self.TRINITY_DIR: str = env["PARASUT_TRINITY_DIR"]
            # ui-library
            self.UI_LIBRARY_NODE_V: str = env["PARASUT_UI_LIBRARY_NODE_V"]
            self.UI_LIBRARY_YARN_V: str = env["PARASUT_UI_LIBRARY_YARN_V"]
            self.UI_LIBRARY_EMBER_PORT: str = env["PARASUT_UI_LIBRARY_EMBER_PORT"]
            self.UI_LIBRARY_DIR: str = env["PARASUT_UI_LIBRARY_DIR"]
            # shared-logic
            self.SHARED_LOGIC_NODE_V: str = env["PARASUT_SHARED_LOGIC_NODE_V"]
            self.SHARED_LOGIC_YARN_V: str = env["PARASUT_SHARED_LOGIC_YARN_V"]
            self.SHARED_LOGIC_EMBER_PORT: str = env["PARASUT_SHARED_LOGIC_EMBER_PORT"]
            self.SHARED_LOGIC_DIR: str = env["PARASUT_SHARED_LOGIC_DIR"]
        except KeyError as e:
            print(f"Please set environment variable: {e}")
            sys.exit(0)
        self._tmux_server: Server
        self._tmux_session_parasut_ws_setup: Session
        self._tmux_session_parasut_ws_editor: Session
        self._third_party_packages: Dict[str, str] = dict(
            npm_cli_login="npm-cli-login",
        )
        self._dep_versions: Dict[str, Dict[str, Any]] = dict(
            ui_library=dict(linked=False, value=""),
            shared_logic=dict(linked=False, value=""),
        )
        self._linking_options: Dict[str, str] = dict(
            ui_library="ui-library",
            shared_logic="shared-logic",
        )
        self._core_commands: Dict[str, str] = dict(
            source_asdf="source ~/.asdf/asdf.sh",
            ember_release="ember release",
            ember_release_all_yes="ember release --yes",
            git_change_branch_master="git checkout master",
            git_change_branch_develop="git checkout develop",
            git_fetch_all="git fetch --all",
            git_pull_origin_master="git pull origin master",
            git_pull_origin_develop="git pull origin develop",
        )
        self._npm_release_commands: Dict[str, str] = dict(
            npm_set_parasut_registry=f"npm config set registry {self.PARASUT_REGISTRY}",
            npm_login="npm login",
            npm_publish="npm publish",
            npm_delete_registry="npm config delete registry",
        )
        self._npm_auto_release_commands: Dict[str, str] = dict(
            npm_set_parasut_registry=f"npm config set registry {self.PARASUT_REGISTRY}",
            npm_login=f"npm-cli-login login -u {self.PARASUT_NPM_USERNAME} -p {self.PARASUT_NPM_PASSWORD} -e {self.PARASUT_NPM_EMAIL} -r {self.PARASUT_REGISTRY}",
            npm_publish="npm publish --verbose",
            npm_delete_registry="npm config delete registry",
        )
        self._worker_commands: Dict[str, str] = dict(
            launch_server_worker="foreman start -m 'worker=1, shoryuken=1, sidekiq_mikro_outbound=1, sidekiq_mikro_outbound=1'",  # noqa: E501
            launch_e_doc_broker_worker="foreman start -m 'shoryuken=1, sidekiq_inbound=1, sidekiq_outbound=1, sidekiq_send=1, sidekiq_fetch_ubl=1, sidekiq_storage=1, sidekiq_other=1, sidekiq_migrations=1'",  # noqa: E501
        )
        self._server_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_ruby_version=f"asdf local ruby {self.SERVER_RUBY_V}",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails="rails server",
            switch_to_phoenix=f"rails runner 'puts Company.find({self.COMPANY_ID}).update!(used_app: \"{self.PHOENIX_SWITCH_NAME}\")'",  # noqa: E501
            switch_to_trinity=f"rails runner 'puts Company.find({self.COMPANY_ID}).update!(used_app: \"{self.TRINITY_SWITCH_NAME}\")'",  # noqa: E501
            switch_to_receipt=f"rails runner 'puts company=Company.find({self.COMPANY_ID}); company.feature_flags[\"using_sales_receipt\"]=true; company.save!'",  # noqa: E501
            switch_to_invoice=f"rails runner 'puts company=Company.find({self.COMPANY_ID}); company.feature_flags[\"using_sales_receipt\"]=false; company.save!'",  # noqa: E501
        )
        self._billing_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_ruby_version=f"asdf local ruby {self.BILLING_RUBY_V}",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails=f"rails server -p {self.BILLING_RAILS_PORT}",
        )
        self._e_doc_broker_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_ruby_version=f"asdf local ruby {self.E_DOC_BROKER_RUBY_V}",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails=f"rails server -p {self.E_DOC_BROKER_RAILS_PORT}",
        )
        self._post_office_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_ruby_version=f"asdf local ruby {self.POST_OFFICE_RUBY_V}",
            launch_sidekiq="bundle exec sidekiq",
            launch_rails=f"rails server -p {self.POST_OFFICE_RAILS_PORT}",
        )
        self._ubl_validator_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_maven_version=f"asdf local maven {self.UBL_VALIDATOR_MAVEN_V}",
            launch_spring_boot="mvn spring-boot:run",
        )
        self._phoenix_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_yarn_version=f"asdf local yarn {self.PHOENIX_YARN_V}",
            choose_node_version=f"asdf local nodejs {self.PHOENIX_NODE_V}",
            ember_serve="PROJECT_TARGET=phoenix ember s",
        )
        self._client_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_yarn_version=f"asdf local yarn {self.CLIENT_YARN_V}",
            choose_node_version=f"asdf local nodejs {self.CLIENT_NODE_V}",
            ember_serve=f"./node_modules/ember-cli/bin/ember s --live-reload-port {self.CLIENT_EMBER_PORT}",  # noqa: E501
        )
        self._trinity_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_yarn_version=f"asdf local yarn {self.TRINITY_YARN_V}",
            choose_node_version=f"asdf local nodejs {self.TRINITY_NODE_V}",
            ember_serve="ember s --live-reload-port 6505",
        )
        self._ui_library_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_yarn_version=f"asdf local yarn {self.UI_LIBRARY_YARN_V}",
            choose_node_version=f"asdf local nodejs {self.UI_LIBRARY_NODE_V}",
            ember_serve=f"PROJECT_TARGET=phoenix ember s --live-reload-port {self.UI_LIBRARY_EMBER_PORT}",  # noqa: E501
        )
        self._shared_logic_commands: Dict[str, str] = dict(
            launch_text_editor=self.PARASUT_CLI_TEXT_EDITOR,
            choose_yarn_version=f"asdf local yarn {self.SHARED_LOGIC_YARN_V}",
            choose_node_version=f"asdf local nodejs {self.SHARED_LOGIC_NODE_V}",
            ember_serve=f"ember s --live-reload-port {self.SHARED_LOGIC_EMBER_PORT}",
        )
        # run tasks
        self._task_run_server = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._server_commands["choose_ruby_version"],
                self._server_commands["launch_rails"],
            ]
        )
        self._task_run_server_sidekiq = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._server_commands["choose_ruby_version"],
                self._server_commands["launch_sidekiq"],
            ]
        )
        self._task_run_billing = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._billing_commands["choose_ruby_version"],
                self._billing_commands["launch_rails"],
            ]
        )
        self._task_run_billing_sidekiq = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._billing_commands["choose_ruby_version"],
                self._billing_commands["launch_sidekiq"],
            ]
        )
        self._task_run_e_doc_broker = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._e_doc_broker_commands["choose_ruby_version"],
                self._e_doc_broker_commands["launch_rails"],
            ]
        )
        self._task_run_e_doc_broker_sidekiq = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._e_doc_broker_commands["choose_ruby_version"],
                self._e_doc_broker_commands["launch_sidekiq"],
            ]
        )
        self._task_run_post_office = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._post_office_commands["choose_ruby_version"],
                self._post_office_commands["launch_rails"],
            ]
        )
        self._task_run_post_office_sidekiq = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._post_office_commands["choose_ruby_version"],
                self._post_office_commands["launch_sidekiq"],
            ]
        )
        self._task_run_ubl_validator = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._ubl_validator_commands["choose_maven_version"],
                self._ubl_validator_commands["launch_spring_boot"],
            ]
        )
        self._task_run_phoenix = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._phoenix_commands["choose_yarn_version"],
                self._phoenix_commands["choose_node_version"],
                self._phoenix_commands["ember_serve"],
            ]
        )
        self._task_run_shared_logic = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._shared_logic_commands["choose_yarn_version"],
                self._shared_logic_commands["choose_node_version"],
                self._shared_logic_commands["ember_serve"],
            ]
        )
        self._task_release_shared_logic = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._shared_logic_commands["choose_yarn_version"],
                self._shared_logic_commands["choose_node_version"],
                self._core_commands["git_change_branch_master"],
                self._core_commands["git_pull_origin_master"],
                self._core_commands["git_fetch_all"],
                self._core_commands["ember_release"],
                self._npm_release_commands["npm_set_parasut_registry"],
                self._npm_release_commands["npm_login"],
                self._npm_release_commands["npm_publish"],
                self._npm_release_commands["npm_delete_registry"],
            ]
        )
        self._task_auto_release_shared_logic = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._shared_logic_commands["choose_yarn_version"],
                self._shared_logic_commands["choose_node_version"],
                self._core_commands["git_change_branch_master"],
                self._core_commands["git_pull_origin_master"],
                self._core_commands["git_fetch_all"],
                self._core_commands["ember_release_all_yes"],
                self._npm_auto_release_commands["npm_set_parasut_registry"],
                self._npm_auto_release_commands["npm_login"],
                self._npm_auto_release_commands["npm_publish"],
                self._npm_auto_release_commands["npm_delete_registry"],
            ]
        )
        self._task_run_trinity = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._trinity_commands["choose_yarn_version"],
                self._trinity_commands["choose_node_version"],
                self._trinity_commands["ember_serve"],
            ]
        )
        self._task_run_ui_library = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._ui_library_commands["choose_yarn_version"],
                self._ui_library_commands["choose_node_version"],
                self._ui_library_commands["ember_serve"],
            ]
        )
        self._task_release_ui_library = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._ui_library_commands["choose_yarn_version"],
                self._ui_library_commands["choose_node_version"],
                self._core_commands["git_change_branch_develop"],
                self._core_commands["git_pull_origin_develop"],
                self._core_commands["git_fetch_all"],
                self._core_commands["ember_release"],
                self._npm_release_commands["npm_set_parasut_registry"],
                self._npm_release_commands["npm_login"],
                self._npm_release_commands["npm_publish"],
                self._npm_release_commands["npm_delete_registry"],
            ]
        )
        self._task_auto_release_ui_library = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._ui_library_commands["choose_yarn_version"],
                self._ui_library_commands["choose_node_version"],
                self._core_commands["git_change_branch_develop"],
                self._core_commands["git_pull_origin_develop"],
                self._core_commands["git_fetch_all"],
                self._core_commands["ember_release_all_yes"],
                self._npm_auto_release_commands["npm_set_parasut_registry"],
                self._npm_auto_release_commands["npm_login"],
                self._npm_auto_release_commands["npm_publish"],
                self._npm_auto_release_commands["npm_delete_registry"],
            ]
        )
        self._task_run_client = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._client_commands["choose_yarn_version"],
                self._client_commands["choose_node_version"],
                self._client_commands["ember_serve"],
            ]
        )
        # switch tasks
        self._task_switch_frontend_to_phoenix = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._server_commands["choose_ruby_version"],
                self._server_commands["switch_to_phoenix"],
            ]
        )
        self._task_switch_frontend_to_trinity = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._server_commands["choose_ruby_version"],
                self._server_commands["switch_to_trinity"],
            ]
        )
        self._task_switch_addling_to_invoice = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._server_commands["choose_ruby_version"],
                self._server_commands["switch_to_invoice"],
            ]
        )
        self._task_switch_addling_to_receipt = " && ".join(
            [
                self._core_commands["source_asdf"],
                self._server_commands["choose_ruby_version"],
                self._server_commands["switch_to_receipt"],
            ]
        )

    def initialize_tmux_server(self) -> None:
        self._tmux_server = Server()

    def run_repo(self, repo_name: str) -> None:
        base_path: str = self._find_repo_path(repo_name)

        self._change_directory(base_path)

        try:
            if repo_name == "server":
                self._run_process([self._task_run_server], show_output=True)
            elif repo_name == "server-sidekiq":
                self._run_process([self._task_run_server_sidekiq], show_output=True)
            elif repo_name == "billing":
                self._run_process([self._task_run_billing], show_output=True)
            elif repo_name == "billing-sidekiq":
                self._run_process([self._task_run_billing_sidekiq], show_output=True)
            elif repo_name == "e-doc-broker":
                self._run_process([self._task_run_e_doc_broker], show_output=True)
            elif repo_name == "e-doc-broker-sidekiq":
                self._run_process(
                    [self._task_run_e_doc_broker_sidekiq], show_output=True
                )
            elif repo_name == "post-office":
                self._run_process([self._task_run_post_office], show_output=True)
            elif repo_name == "post-office-sidekiq":
                self._run_process(
                    [self._task_run_post_office_sidekiq], show_output=True
                )
            elif repo_name == "ubl-validator":
                self._run_process([self._task_run_ubl_validator], show_output=True)
            elif repo_name == "phoenix":
                self._run_process([self._task_run_phoenix], show_output=True)
            elif repo_name == "shared-logic":
                self._run_process([self._task_run_shared_logic], show_output=True)
            elif repo_name == "trinity":
                self._run_process([self._task_run_trinity], show_output=True)
            elif repo_name == "ui-library":
                self._run_process([self._task_run_ui_library], show_output=True)
            elif repo_name == "client":
                self._run_process([self._task_run_client], show_output=True)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)

    def release_repo(
        self, target_repo: str, show_output: bool, auto_login: bool
    ) -> None:
        target_path: str = self._find_repo_path(target_repo)

        self._check_npm_package_installed(self._third_party_packages["npm_cli_login"])
        self._change_directory(target_path)

        try:
            if target_repo == "shared-logic":
                if auto_login is True:
                    self._run_process(
                        [self._task_auto_release_shared_logic], show_output=show_output
                    )
                    if show_output is False:
                        console.print(":ok_hand: Target repo has been released.")
                else:
                    self._run_process(
                        [self._task_release_shared_logic], show_output=show_output
                    )
                    if show_output is False:
                        console.print(":ok_hand: Target repo has been released.")
            elif target_repo == "ui-library":
                if auto_login is True:
                    self._run_process(
                        [self._task_auto_release_ui_library], show_output=show_output
                    )
                    if show_output is False:
                        console.print(":ok_hand: Target repo has been released.")
                else:
                    self._run_process(
                        [self._task_release_ui_library], show_output=show_output
                    )
                    if show_output is False:
                        console.print(":ok_hand: Target repo has been released.")
        except KeyboardInterrupt:
            console.print(
                ":pile_of_poo: You interrupted process. \
                          Manually check your demand steps."
            )
            sys.exit(0)
        except Exception as e:
            print(e)

    def create_parasut_ws_setup(self, repos: List[str]) -> None:
        session: Optional[Session]

        # get or create session
        try:
            session = self._tmux_server.find_where({"session_name": "parasut-ws-setup"})
        except LibTmuxException:
            session = None
        finally:
            if session:
                self._tmux_session_parasut_ws_setup = session
            else:
                self._tmux_session_parasut_ws_setup = self._tmux_server.new_session(
                    session_name="parasut-ws-setup", kill_session=True, attach=False
                )

        # launch relative repos
        for repo_name in repos:
            if repo_name == "server":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.SERVER_DIR}")
                self._launch_parasut_server_repo()
            elif repo_name == "billing":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.BILLING_DIR}")
                self._launch_parasut_billing_repo()
            elif repo_name == "e-doc-broker":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.E_DOC_BROKER_DIR}"
                )
                self._launch_parasut_e_doc_broker_repo()
            elif repo_name == "post-office":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.POST_OFFICE_DIR}"
                )
                self._launch_parasut_post_office_repo()
            elif repo_name == "ubl-validator":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.UBL_VALIDATOR_DIR}"
                )
                self._launch_parasut_ubl_validator_repo()
            elif repo_name == "phoenix":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.PHOENIX_DIR}")
                self._launch_parasut_phoenix_repo()
            elif repo_name == "client":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.CLIENT_DIR}")
                self._launch_parasut_client_repo()
            elif repo_name == "trinity":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.TRINITY_DIR}")
                self._launch_parasut_trinity_repo()
            elif repo_name == "ui-library":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.UI_LIBRARY_DIR}")
                self._launch_parasut_ui_library_repo()
            elif repo_name == "shared-logic":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.SHARED_LOGIC_DIR}"
                )
                self._launch_parasut_shared_logic_repo()

        # kill the first empty window if new session initialized
        if not session:
            self._tmux_session_parasut_ws_setup.select_window(1).kill_window()

    def create_parasut_ws_editor(self, repos: List[str]) -> None:
        session: Optional[Session]

        # get or create session
        try:
            session = self._tmux_server.find_where(
                {"session_name": "parasut-ws-editor"}
            )
        except LibTmuxException:
            session = None
        finally:
            if session:
                self._tmux_session_parasut_ws_editor = session
            else:
                self._tmux_session_parasut_ws_editor = self._tmux_server.new_session(
                    session_name="parasut-ws-editor", kill_session=True, attach=False
                )

        # launch relative repos
        for repo_name in repos:
            if repo_name == "server":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.SERVER_DIR}")
                self._launch_parasut_server_editor()
            elif repo_name == "billing":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.BILLING_DIR}")
                self._launch_parasut_billing_editor()
            elif repo_name == "e-doc-broker":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.E_DOC_BROKER_DIR}"
                )
                self._launch_parasut_e_doc_broker_editor()
            elif repo_name == "post-office":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.POST_OFFICE_DIR}"
                )
                self._launch_parasut_post_office_editor()
            elif repo_name == "ubl-validator":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.UBL_VALIDATOR_DIR}"
                )
                self._launch_parasut_ubl_validator_editor()
            elif repo_name == "phoenix":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.PHOENIX_DIR}")
                self._launch_parasut_phoenix_editor()
            elif repo_name == "client":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.CLIENT_DIR}")
                self._launch_parasut_client_editor()
            elif repo_name == "trinity":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.TRINITY_DIR}")
                self._launch_parasut_trinity_editor()
            elif repo_name == "ui-library":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.UI_LIBRARY_DIR}")
                self._launch_parasut_ui_library_editor()
            elif repo_name == "shared-logic":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.SHARED_LOGIC_DIR}"
                )
                self._launch_parasut_shared_logic_editor()

        # kill the first empty window if new session initialized
        if not session:
            self._tmux_session_parasut_ws_editor.select_window(1).kill_window()
        self._tmux_session_parasut_ws_editor.select_window(1)

    def create_parasut_ws_worker(self, workers: List[str]) -> None:
        session: Optional[Session]

        # get or create session
        try:
            session = self._tmux_server.find_where(
                {"session_name": "parasut-ws-worker"}
            )
        except LibTmuxException:
            session = None
        finally:
            if session:
                self._tmux_session_parasut_ws_worker = session
            else:
                self._tmux_session_parasut_ws_worker = self._tmux_server.new_session(
                    session_name="parasut-ws-worker", kill_session=True, attach=False
                )

        # launch relative repos
        for worker in workers:
            if worker == "server-worker":
                self._change_directory(f"{self.PARASUT_BASE_DIR}/{self.SERVER_DIR}")
                self._launch_parasut_server_worker()
            elif worker == "e-doc-broker-worker":
                self._change_directory(
                    f"{self.PARASUT_BASE_DIR}/{self.E_DOC_BROKER_DIR}"
                )
                self._launch_parasut_e_doc_broker_worker()

        # kill the first empty window if new session initialized
        if not session:
            self._tmux_session_parasut_ws_worker.select_window(1).kill_window()
        self._tmux_session_parasut_ws_worker.select_window(1)

    def switch_server_rails_frontend(self, target_repo: str, show_output: bool) -> None:
        server_repo: str = f"{self.PARASUT_BASE_DIR}/{self.SERVER_DIR}"

        self._change_directory(server_repo)

        try:
            if target_repo == "phoenix":
                self._run_process(
                    tasks=[self._task_switch_frontend_to_phoenix],
                    show_output=show_output,
                )
                if show_output is False:
                    console.print(":clinking_beer_mugs: Demand accomplished.")
            if target_repo == "trinity":
                self._run_process(
                    tasks=[self._task_switch_frontend_to_trinity],
                    show_output=show_output,
                )
                if show_output is False:
                    console.print(":clinking_beer_mugs: Demand accomplished.")
        except KeyboardInterrupt:
            console.print(
                ":pile_of_poo: You interrupted process. \
                          Manually check your demand steps."
            )
            sys.exit(0)

    def switch_server_rails_addling(
        self, target_addling: str, show_output: bool
    ) -> None:
        server_repo: str = f"{self.PARASUT_BASE_DIR}/{self.SERVER_DIR}"

        self._change_directory(server_repo)

        try:
            if target_addling == "receipt":
                self._run_process(
                    tasks=[self._task_switch_addling_to_receipt],
                    show_output=show_output,
                )
                if show_output is False:
                    console.print(":clinking_beer_mugs: Demand accomplished.")
            if target_addling == "invoice":
                self._run_process(
                    tasks=[self._task_switch_addling_to_invoice],
                    show_output=show_output,
                )
                if show_output is False:
                    console.print(":clinking_beer_mugs: Demand accomplished.")
        except KeyboardInterrupt:
            console.print(
                ":pile_of_poo: You interrupted process. \
                          Manually check your demand steps."
            )
            sys.exit(0)

    def do_linking(
        self, base_repo: str, target_repos: List[str], show_output: bool
    ) -> None:
        base_path: str = self._find_repo_path(base_repo)
        dep_key: str = ""
        dep_value: str = ""
        target_path: str = ""
        json_file: str = ""

        self._initialize_dep_versions(base_repo)
        self._change_directory(base_path)

        for repo_name in target_repos:
            if repo_name == "ui-library":
                dep_key = "ui-library"
                dep_value = f"link:../{repo_name}"
                target_path = f"{self.PARASUT_BASE_DIR}/{self.UI_LIBRARY_DIR}"
                json_file = "package.json"

                if self._dep_versions["ui_library"]["linked"] is True:
                    print(
                        f"{repo_name} has been linked before. \
                          Try --list to check linked repos."
                    )
                else:
                    self._dep_versions["ui_library"][
                        "value"
                    ] = self._change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["ui_library"]["linked"] = True

                    self._store_linking_info(self._dep_versions)
                    self._apply_package_changes(show_output=show_output)
                    if show_output is False:
                        console.print(":ok_hand: Base repo linked.")
                    self._change_directory(target_path)
                    self._apply_package_changes(show_output=show_output, force=True)
                    if show_output is False:
                        console.print(":ok_hand: Target repo reloaded.")
                    self._change_directory(base_path)
                    if show_output is False:
                        console.print(":clinking_beer_mugs: Demand accomplished.")
            elif repo_name == "shared-logic":
                dep_key = "shared-logic"
                dep_value = f"link:../{repo_name}"
                target_path = f"{self.PARASUT_BASE_DIR}/{self.SHARED_LOGIC_DIR}"
                json_file = "package.json"

                if self._dep_versions["shared_logic"]["linked"] is True:
                    print(
                        f"{repo_name} has been linked before. \
                          Try --list to check linked repos."
                    )
                else:
                    self._dep_versions["shared_logic"][
                        "value"
                    ] = self._change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["shared_logic"]["linked"] = True

                    self._store_linking_info(self._dep_versions)
                    self._apply_package_changes(show_output=show_output)
                    if show_output is False:
                        console.print(":ok_hand: Base repo linked.")
                    self._change_directory(target_path)
                    self._apply_package_changes(show_output=show_output, force=True)
                    if show_output is False:
                        console.print(":ok_hand: Target repo reloaded.")
                    self._change_directory(base_path)
                    if show_output is False:
                        console.print(":clinking_beer_mugs: Demand accomplished.")

    def undo_linking(self, base_repo: str, repos: List[str], show_output: bool) -> None:
        base_path: str = self._find_repo_path(base_repo)
        dep_key: str = ""
        dep_value: str = ""
        target_path: str = ""
        json_file: str = ""

        self._initialize_dep_versions(base_repo)
        self._change_directory(base_path)

        for repo_name in repos:
            if repo_name == "ui-library":
                dep_key = "ui-library"
                dep_value = self._dep_versions["ui_library"]["value"]
                target_path = f"{self.PARASUT_BASE_DIR}/{self.UI_LIBRARY_DIR}"
                json_file = "package.json"

                if self._dep_versions["ui_library"]["linked"] is False:
                    print(
                        f"{repo_name} has not been linked before. \
                          Try listing linked repos."
                    )
                else:
                    self._change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["ui_library"]["linked"] = False

                    self._apply_package_changes(show_output=show_output)
                    if show_output is False:
                        console.print(":ok_hand: Base repo unlinked.")
                    self._change_directory(target_path)
                    self._apply_package_changes(show_output=show_output, force=True)
                    if show_output is False:
                        console.print(":ok_hand: Undoed target repo reloaded.")
                    self._change_directory(base_path)
                    if show_output is False:
                        console.print(":clinking_beer_mugs: Demand accomplished.")
            elif repo_name == "shared-logic":
                dep_key = "shared-logic"
                dep_value = self._dep_versions["shared_logic"]["value"]
                target_path = f"{self.PARASUT_BASE_DIR}/{self.SHARED_LOGIC_DIR}"
                json_file = "package.json"

                if self._dep_versions["shared_logic"]["linked"] is False:
                    print(
                        f"{repo_name} has not been linked before. \
                          Try listing linked repos."
                    )
                else:
                    self._change_dependency_value(
                        dep_json_file=json_file, dep_key=dep_key, dep_value=dep_value
                    )
                    self._dep_versions["shared_logic"]["linked"] = False

                    self._apply_package_changes(show_output=show_output)
                    if show_output is False:
                        console.print(":ok_hand: Base repo unlinked.")
                    self._change_directory(target_path)
                    self._apply_package_changes(show_output=show_output, force=True)
                    if show_output is False:
                        console.print(":ok_hand: Undoed target repo reloaded.")
                    self._change_directory(base_path)
                    if show_output is False:
                        console.print(":clinking_beer_mugs: Demand accomplished.")

    def get_linked_repos(self, base_repo: str) -> None:
        for key, value in self._dep_versions.items():
            if self._dep_versions[key]["linked"]:
                print(key)
        else:
            print("There is no repo linking to this repo.")

    def get_pkg_version(self) -> None:
        print(parasut_cli.__version__)

    def _check_npm_package_installed(self, pkg_name: str):
        command = f"npm list -g --depth=0 | grep {pkg_name}"

        try:
            output = self._run_process(tasks=[command], show_output=False).stdout
        except subprocess.CalledProcessError:
            console.print(f":thumbs_down: You must install '{pkg_name}' package.")
            sys.exit(0)

    def _run_process(self, tasks: List[str], show_output: bool):
        if show_output is False:
            with console.status("[bold green] Working on process..."):
                for task in tasks:
                    result = subprocess.run(
                        ["/bin/zsh", "-c", f"{task}"],
                        capture_output=True,
                        text=True,
                    )
                    result.check_returncode()
                    return result
        else:
            for task in tasks:
                subprocess.run(
                    ["/bin/zsh", "-c", f"{task}"],
                )

    def _apply_package_changes(self, show_output: bool, force: bool = False) -> None:
        attempts = 0
        command = f"yarn install{' --force' if force else ''}"

        while attempts < 3:
            try:
                self._run_process(tasks=[command], show_output=show_output)
                break
            except subprocess.CalledProcessError:
                if show_output is False:
                    console.print(
                        ":thumbs_down: Yarn had a problem with an dependent package."
                    )
                    if attempts == 2:
                        sleep(1)
                        console.print(":goblin: &$!#%")
                        sleep(1)
                        console.print(":goblin::fire: Trying last time..")
                    else:
                        console.print(":fire: Trying again..")
                attempts += 1
        else:
            console.print(
                ":broken_heart: Yarn couldn't install dependencies on related repo."
            )

    def _change_dependency_value(
        self, dep_json_file: str, dep_key: str, dep_value: str
    ) -> str:
        with open(dep_json_file, "r") as json_file:
            data = json.load(json_file)
            dep_ver = data["devDependencies"][dep_key]
            data["devDependencies"][dep_key] = dep_value

        with open(dep_json_file, "w+") as json_file:
            json_file.write(json.dumps(data, indent=2))

        return dep_ver

    def _find_repo_path(self, repo_name: str) -> str:
        if repo_name == "server" or "server" in repo_name:
            return f"{self.PARASUT_BASE_DIR}/{self.SERVER_DIR}"
        elif repo_name == "billing" or "billing" in repo_name:
            return f"{self.PARASUT_BASE_DIR}/{self.BILLING_DIR}"
        elif repo_name == "e-doc-broker" or "e-doc-broker" in repo_name:
            return f"{self.PARASUT_BASE_DIR}/{self.E_DOC_BROKER_DIR}"
        elif repo_name == "post-office" or "post-office" in repo_name:
            return f"{self.PARASUT_BASE_DIR}/{self.POST_OFFICE_DIR}"
        elif repo_name == "ubl-validator" or "ubl-validator" in repo_name:
            return f"{self.PARASUT_BASE_DIR}/{self.UBL_VALIDATOR_DIR}"
        elif repo_name == "client":
            return f"{self.PARASUT_BASE_DIR}/{self.CLIENT_DIR}"
        elif repo_name == "phoenix":
            return f"{self.PARASUT_BASE_DIR}/{self.PHOENIX_DIR}"
        elif repo_name == "shared-logic":
            return f"{self.PARASUT_BASE_DIR}/{self.SHARED_LOGIC_DIR}"
        elif repo_name == "trinity":
            return f"{self.PARASUT_BASE_DIR}/{self.TRINITY_DIR}"
        elif repo_name == "ui-library":
            return f"{self.PARASUT_BASE_DIR}/{self.UI_LIBRARY_DIR}"
        else:
            raise Exception(
                "Exiting because of an error: wrong repo path. couldn't find the repo"
            )

    def _store_linking_info(self, dep_versions: Dict) -> None:
        pickle_file_path: str = f"{APP_DIR}/state/link_info.pickle"

        with open(pickle_file_path, "wb") as handle:
            pickle.dump(dep_versions, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def _initialize_dep_versions(self, base_repo: str) -> None:
        pickle_file_path: str = f"{APP_DIR}/state/link_info.pickle"

        try:
            with open(pickle_file_path, "rb") as handle:
                self._dep_versions = pickle.load(handle)
        except FileNotFoundError:
            with open(pickle_file_path, "wb") as handle:
                pickle.dump(
                    self._dep_versions, handle, protocol=pickle.HIGHEST_PROTOCOL
                )

        for i, j in self._linking_options.items():
            if self._is_linked(base_repo=base_repo, dep_key=j):
                self._dep_versions[i]["linked"] = True
            else:
                self._dep_versions[i]["linked"] = False

    def _is_linked(self, base_repo: str, dep_key: str) -> bool:
        base_path: str = self._find_repo_path(base_repo)
        checking_word: str = "link"
        json_file: str = "package.json"

        self._change_directory(base_path)

        with open(json_file, "r") as file:
            data = json.load(file)
            if checking_word in data["devDependencies"][dep_key]:
                return True
            else:
                return False

    def _change_directory(self, path: str) -> None:
        os.chdir(os.path.expanduser(path))

    def _launch_parasut_server_repo(self) -> None:
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

    def _launch_parasut_server_editor(self) -> None:
        server_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="server"
        )
        server_pane: Pane = server_window.attached_pane

        server_pane.send_keys(
            " && ".join(
                [
                    self._server_commands["choose_ruby_version"],
                    self._server_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_server_worker(self) -> None:
        server_worker_window: Window = self._tmux_session_parasut_ws_worker.new_window(
            attach=False, window_name="server_worker"
        )
        server_worker_pane: Pane = server_worker_window.attached_pane

        server_worker_pane.send_keys(
            " && ".join(
                [
                    self._server_commands["choose_ruby_version"],
                    self._worker_commands["launch_server_worker"],
                ]
            )
        )

    def _launch_parasut_billing_repo(self) -> None:
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

    def _launch_parasut_billing_editor(self) -> None:
        billing_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="billing"
        )
        billing_pane: Pane = billing_window.attached_pane

        billing_pane.send_keys(
            " && ".join(
                [
                    self._billing_commands["choose_ruby_version"],
                    self._billing_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_e_doc_broker_repo(self) -> None:
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

    def _launch_parasut_e_doc_broker_editor(self) -> None:
        e_doc_broker_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="e_doc_broker"
        )
        e_doc_broker_pane: Pane = e_doc_broker_window.attached_pane

        e_doc_broker_pane.send_keys(
            " && ".join(
                [
                    self._e_doc_broker_commands["choose_ruby_version"],
                    self._e_doc_broker_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_e_doc_broker_worker(self) -> None:
        e_doc_broker_worker_window: Window = (
            self._tmux_session_parasut_ws_worker.new_window(
                attach=False, window_name="e_doc_broker_worker"
            )
        )
        e_doc_broker_worker_pane: Pane = e_doc_broker_worker_window.attached_pane

        e_doc_broker_worker_pane.send_keys(
            " && ".join(
                [
                    self._e_doc_broker_commands["choose_ruby_version"],
                    self._worker_commands["launch_e_doc_broker_worker"],
                ]
            )
        )

    def _launch_parasut_post_office_repo(self) -> None:
        post_office_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="post_office"
        )
        post_office_pane: Pane = post_office_window.attached_pane
        post_office_sidekiq_pane: Pane = post_office_window.split_window(vertical=False)

        post_office_window.select_layout("tiled")
        # panes
        post_office_pane.send_keys(
            " && ".join(
                [
                    self._post_office_commands["choose_ruby_version"],
                    self._post_office_commands["launch_rails"],
                ]
            )
        )
        post_office_sidekiq_pane.send_keys(
            " && ".join(
                [
                    self._post_office_commands["choose_ruby_version"],
                    self._post_office_commands["launch_sidekiq"],
                ]
            )
        )

    def _launch_parasut_post_office_editor(self) -> None:
        post_office_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="post_office"
        )
        post_office_pane: Pane = post_office_window.attached_pane

        post_office_pane.send_keys(
            " && ".join(
                [
                    self._post_office_commands["choose_ruby_version"],
                    self._post_office_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_ubl_validator_repo(self) -> None:
        ubl_validator_window: Window = self._tmux_session_parasut_ws_setup.new_window(
            attach=False, window_name="ubl_validator"
        )
        ubl_validator_pane: Pane = ubl_validator_window.attached_pane

        ubl_validator_pane.send_keys(
            " && ".join(
                [
                    self._ubl_validator_commands["choose_maven_version"],
                    self._ubl_validator_commands["launch_spring_boot"],
                ]
            )
        )

    def _launch_parasut_ubl_validator_editor(self) -> None:
        ubl_validator_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="ubl_validator"
        )
        ubl_validator_pane: Pane = ubl_validator_window.attached_pane

        ubl_validator_pane.send_keys(
            " && ".join(
                [
                    self._ubl_validator_commands["choose_maven_version"],
                    self._ubl_validator_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_phoenix_repo(self) -> None:
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

    def _launch_parasut_phoenix_editor(self) -> None:
        phoenix_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="phoenix"
        )
        phoenix_pane: Pane = phoenix_window.attached_pane

        phoenix_pane.send_keys(
            " && ".join(
                [
                    self._phoenix_commands["choose_yarn_version"],
                    self._phoenix_commands["choose_node_version"],
                    self._phoenix_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_client_repo(self) -> None:
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

    def _launch_parasut_client_editor(self) -> None:
        client_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="client"
        )
        client_pane: Pane = client_window.attached_pane

        client_pane.send_keys(
            " && ".join(
                [
                    self._client_commands["choose_yarn_version"],
                    self._client_commands["choose_node_version"],
                    self._client_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_trinity_repo(self) -> None:
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

    def _launch_parasut_trinity_editor(self) -> None:
        trinity_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="trinity"
        )
        trinity_pane: Pane = trinity_window.attached_pane

        trinity_pane.send_keys(
            " && ".join(
                [
                    self._trinity_commands["choose_yarn_version"],
                    self._trinity_commands["choose_node_version"],
                    self._trinity_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_ui_library_repo(self) -> None:
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

    def _launch_parasut_ui_library_editor(self) -> None:
        ui_library_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="ui_library"
        )
        ui_library_pane: Pane = ui_library_window.attached_pane

        ui_library_pane.send_keys(
            " && ".join(
                [
                    self._ui_library_commands["choose_yarn_version"],
                    self._ui_library_commands["choose_node_version"],
                    self._ui_library_commands["launch_text_editor"],
                ]
            )
        )

    def _launch_parasut_shared_logic_repo(self) -> None:
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

    def _launch_parasut_shared_logic_editor(self) -> None:
        shared_logic_window: Window = self._tmux_session_parasut_ws_editor.new_window(
            attach=False, window_name="shared_logic"
        )
        shared_logic_pane: Pane = shared_logic_window.attached_pane

        shared_logic_pane.send_keys(
            " && ".join(
                [
                    self._shared_logic_commands["choose_yarn_version"],
                    self._shared_logic_commands["choose_node_version"],
                    self._shared_logic_commands["launch_text_editor"],
                ]
            )
        )
