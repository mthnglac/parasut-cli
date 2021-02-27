import argparse
import sys
from parasut_cli.utils.invoker import Invoker
from parasut_cli.utils.receiver import Receiver
from parasut_cli.commands.start import StartCommand
from parasut_cli.commands.link import LinkCommand


def main():
    parser = argparse.ArgumentParser("PROG")
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="sub-command help")
    parser_a = subparsers.add_parser("start", help="start help")
    parser_a.add_argument('-r', '--repo', dest='starting_repos', type=str, nargs='*', choices=['server', 'billing', 'phoenix', 'shared-logic', 'trinity', 'ui-library', 'client', 'e-doc-broker'], required=True, metavar='<repo-name>', help='an repository name for setting up the workspace')
    parser_b = subparsers.add_parser("link", help="link help")
    parser_b.add_argument('-r', '--repo', dest='linking_repos', type=str, nargs='*', choices=['ui-library', 'shared-logic'], required=True, metavar='<repo-name>', help='an reporitory name for linking it to current repository')
    args = parser.parse_args()

    invoker = Invoker()
    receiver = Receiver()

    invoker.do_something_important(StartCommand(receiver, args.starting_repos))
    invoker.do_something_important(LinkCommand(receiver, args.linking_repos))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
