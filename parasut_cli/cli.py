import argparse
import sys
from parasut_cli.utils.invoker import Invoker
from parasut_cli.utils.receiver import Receiver
from parasut_cli.commands.start import StartCommand


def main():
    parser = argparse.ArgumentParser("PROG")
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="sub-command help")
    parser_a = subparsers.add_parser("start", help="start help")
    parser_a.add_argument('-r', '--repo', type=str, nargs='*', required=True, help='repo help')
    args = parser.parse_args()

    invoker = Invoker()
    receiver = Receiver()

    invoker.do_something_important(StartCommand(receiver, args.repo))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
