from __future__ import annotations
from lib.concrete_builder import ConcreteBuilder
from lib.director import Director
import argparse

from lib.command_pattern.invoker import Invoker
from lib.command_pattern.receiver import Receiver
from lib.command_pattern.complex_command import ComplexCommand


if __name__ == "__main__":
    # builder = ConcreteBuilder()
    # director = Director()
    # director.builder = builder

    # print("Standard basic project: ")
    # director.build_minimal_viable_project()
    # director.get_list_repos()

    # print("\n")

    # print("Standard full featured project: ")
    # director.build_full_featured_project()
    # director.get_list_repos()


    # parser = argparse.ArgumentParser()
    # subparsers = parser.add_subparsers(help="help for sub-command")

    # parser_a = subparsers.add_parser("start", help="help for start command")
    # parser.add_argument('-r', '--repo', type=str, nargs='*', required=True, help='repo name')
    # args = parser.parse_args("start")

    # if (args.repo):
        # print(args.repo)

    # director.build_project(args)

    invoker = Invoker()
    receiver = Receiver()
    invoker.set_on_finish(ComplexCommand(receiver, "trinity", "ui-library"))
    invoker.do_something_important()
