from __future__ import annotations
from .builder import Builder
from argparse import Namespace


class Director:
    def __init__(self) -> None:
        self._builder: Builder

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def get_list_repos(self) -> None:
        self.builder.get_list_repos()

    def build_minimal_viable_project(self) -> None:
        self.builder.launch_server()
        self.builder.launch_server_sidekiq()
        self.builder.launch_billing()
        self.builder.launch_billing_sidekiq()
        self.builder.launch_phoenix()

    def build_full_featured_project(self) -> None:
        self.builder.launch_server()
        self.builder.launch_server_sidekiq()
        self.builder.launch_billing()
        self.builder.launch_billing_sidekiq()
        self.builder.launch_phoenix()
        self.builder.launch_trinity()
        self.builder.launch_ui_library()

    def build_project(self, args: Namespace) -> None:
        print(args)
