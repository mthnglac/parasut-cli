from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from .project import Project


class Builder(ABC):

    @abstractproperty
    def project(self) -> Project:
        pass

    @abstractmethod
    def get_list_repos(self) -> None:
        pass

    @abstractmethod
    def launch_phoenix(self) -> None:
        pass

    @abstractmethod
    def launch_shared_logic(self) -> None:
        pass

    @abstractmethod
    def launch_trinity(self) -> None:
        pass

    @abstractmethod
    def launch_ui_library(self) -> None:
        pass

    @abstractmethod
    def launch_client(self) -> None:
        pass

    @abstractmethod
    def launch_server(self) -> None:
        pass

    @abstractmethod
    def launch_server_sidekiq(self) -> None:
        pass

    @abstractmethod
    def launch_billing(self) -> None:
        pass

    @abstractmethod
    def launch_billing_sidekiq(self) -> None:
        pass
