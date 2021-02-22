from __future__ import annotations
from .builder import Builder
from .project import Project


class ConcreteBuilder(Builder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._project = Project()

    @property
    def project(self) -> Project:
        project = self._project
        self.reset()
        return project

    def get_list_repos(self) -> None:
        self._project.list_repos()

    def launch_phoenix(self) -> None:
        # self._project.add("phoenix")
        self._project.set_directory("~/Code/development/parasutcom/phoenix/")
        self._project.choose_yarn_version("1.21.1")
        self._project.choose_node_version("8.16.0")
        self._project.execute("PROJECT_TARGET=phoenix ember s")

    def launch_shared_logic(self) -> None:
        # self._project.add("shared-logic")
        self._project.set_directory("~/Code/development/parasutcom/shared-logic/")
        self._project.choose_yarn_version("1.21.1")
        self._project.choose_node_version("8.16.0")
        self._project.execute("PROJECT_TARGET=phoenix ember s --live-reload-port 6515")

    def launch_trinity(self) -> None:
        # self._project.add("trinity")
        self._project.set_directory("~/Code/development/parasutcom/trinity/")
        self._project.choose_yarn_version("1.21.1")
        self._project.choose_node_version("8.16.0")
        self._project.execute("ember s --live-reload-port 6510")

    def launch_ui_library(self) -> None:
        # self._project.add("ui-library")
        self._project.set_directory("~/Code/development/parasutcom/ui-library/")
        self._project.choose_yarn_version("1.21.1")
        self._project.choose_node_version("8.16.0")
        self._project.execute("PROJECT_TARGET=phoenix ember s --live-reload-port 6500")

    def launch_client(self) -> None:
        # self._project.add("client")
        self._project.set_directory("~/Code/development/parasutcom/client/")
        self._project.choose_yarn_version("1.21.1")
        self._project.choose_node_version("0.11.16")
        self._project.execute(
            "./node_modules/ember-cli/bin/ember s --live-reload-port 6505"
        )

    def launch_server(self) -> None:
        # self._project.add("server")
        self._project.set_directory("~/Code/development/parasutcom/server/")
        self._project.choose_ruby_version("2.6.6")
        self._project.execute("rails server")

    def launch_server_sidekiq(self) -> None:
        # self._project.add("server-sidekiq")
        self._project.set_directory("~/Code/development/parasutcom/server/")
        self._project.choose_ruby_version("2.6.6")
        self._project.execute("bundle exec sidekiq")

    def launch_billing(self) -> None:
        # self._project.add("billing")
        self._project.set_directory("~/Code/development/parasutcom/billing/")
        self._project.choose_ruby_version("2.4.2")
        self._project.execute("rails server -p 4002")

    def launch_billing_sidekiq(self) -> None:
        # self._project.add("billing-sidekiq")
        self._project.set_directory("~/Code/development/parasutcom/billing/")
        self._project.choose_ruby_version("2.4.2")
        self._project.execute("bundle exec sidekiq")
