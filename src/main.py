from __future__ import annotations
from lib.invoker import Invoker
from lib.receiver import Receiver
from commands.start import Start
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="help for sub-command")

    parser_a = subparsers.add_parser("start", help="help for start command")
    parser.add_argument('-r', '--repo', type=str, nargs='*', required=True, help='repo name')
    # args = parser.parse_args("start")

    invoker = Invoker()
    receiver = Receiver()
    invoker.set_on_finish(Start(receiver, "trinity", "ui-library"))
    invoker.do_something_important()
