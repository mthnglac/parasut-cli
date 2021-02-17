from __future__ import annotations
from typing import List
import subprocess
import os


class Project():

    def __init__(self) -> None:
        self.repos: List[str] = []

    def add(self, repo: str) -> None:
        self.repos.append(repo)

    def list_repos(self) -> None:
        print(f"Project repos: {', '.join(self.repos)}", end="")

    def choose_yarn_version(self, version: str) -> None:
        subprocess.run(['/bin/zsh', '-i', '-c', 'yvm use {0}'.format(version)])

    def choose_node_version(self, version: str) -> None:
        subprocess.run(['/bin/zsh', '-i', '-c', 'nvm use {0}'.format(version)])

    def choose_ruby_version(self, version: str) -> None:
        subprocess.run(['/bin/zsh', '-i', '-c', 'rvm use {0}'.format(version)])

    def set_directory(self, path: str) -> None:
        os.chdir(os.path.expanduser(path))

    def execute(self, command: str) -> None:
        subprocess.run(['/bin/zsh', '-i', '-c', '{0}'.format(command)])
