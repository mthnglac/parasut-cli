import argparse
import sys

from parasut_cli.utils.invoker import Invoker
from parasut_cli.utils.receiver import Receiver
from parasut_cli.commands.start import StartCommand
from parasut_cli.commands.link import LinkCommand


def main():
    parent_parser = argparse.ArgumentParser("Parasut CLI")
    subparsers = parent_parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="sub-command help",
        dest="subcommand",
    )

    # start command
    parser_start = subparsers.add_parser(
        "start", help="an repository name for setting up the workspace"
    )
    parser_start.add_argument(
        "-e",
        "--edit",
        dest="edit_repos",
        metavar="<repo-name>",
        type=str,
        nargs="+",
        choices=[
            "server",
            "billing",
            "phoenix",
            "shared-logic",
            "trinity",
            "ui-library",
            "client",
            "e-doc-broker",
        ],
        help="a repository name to open in editor",
    )
    parser_start.add_argument(
        "-s",
        "--setup",
        dest="setup_repos",
        metavar="<repo-name>",
        type=str,
        nargs="+",
        choices=[
            "server",
            "billing",
            "phoenix",
            "shared-logic",
            "trinity",
            "ui-library",
            "client",
            "e-doc-broker",
        ],
        help="a repository name to launch",
    )

    # link command
    parser_link = subparsers.add_parser("link", help="link help")
    group_link = parser_link.add_mutually_exclusive_group(required=True)
    parser_link.add_argument(
        "-b",
        "--base",
        dest="base_repo",
        metavar="<repo-name>",
        type=str,
        nargs=1,
        choices=["phoenix", "trinity"],
        required=True,
        help="an base reporitory name for linking target repository. Use this with -t option",
    )
    group_link.add_argument(
        "-t",
        "--target",
        dest="target_repos",
        metavar="<repo-name>",
        type=str,
        nargs="+",
        choices=["ui-library", "shared-logic"],
        help="an target reporitory name for linking it to base repository",
    )
    group_link.add_argument(
        "-u",
        "--undo",
        dest="undo_linked_repos",
        metavar="<repo-name>",
        type=str,
        nargs="+",
        choices=["ui-library", "shared-logic"],
        help="an reporitory name for unlinking it",
    )
    group_link.add_argument(
        "-l",
        "--list",
        dest="list_linked_repos",
        action="store_true",
        help="listing linked repos of base repo",
    )

    args = parent_parser.parse_args()

    invoker = Invoker()
    receiver = Receiver()

    if hasattr(args, "subcommand") and args.subcommand == "start":
        if getattr(args, "edit_repos", False) or getattr(args, "setup_repos", False):
            invoker.do_something_important(
                StartCommand(
                    receiver,
                    setup_repos=args.setup_repos,
                    edit_repos=args.edit_repos,
                )
            )
        else:
            parser_start.print_help()
    elif hasattr(args, "subcommand") and args.subcommand == "link":
        if getattr(args, "target_repos", False) or getattr(args, "undo_linked_repos", False) or getattr(args, "list_linked_repos", False):
            invoker.do_something_important(
                LinkCommand(
                    receiver,
                    base_repo=args.base_repo,
                    target_repos=args.target_repos,
                    undo_linked_repos=args.undo_linked_repos,
                    list_linked_repos=args.list_linked_repos,
                )
            )
        else:
            parser_link.print_help()
    else:
        parent_parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
