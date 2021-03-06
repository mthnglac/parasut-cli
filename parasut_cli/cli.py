import argparse
import sys

from parasut_cli.utils.invoker import Invoker
from parasut_cli.utils.receiver import Receiver
from parasut_cli.commands.start import StartCommand
from parasut_cli.commands.link import LinkCommand
from parasut_cli.commands.switch import SwitchCommand


def main():
    parent_parser = argparse.ArgumentParser("Parasut CLI")
    subparsers = parent_parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="sub-command help",
        dest="subcommand",
    )

    # start command parser
    parser_start = subparsers.add_parser(
        "start", help="command for setting up the workspace"
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

    # link command parser
    parser_link = subparsers.add_parser("link", help="command for linking")
    group_link = parser_link.add_mutually_exclusive_group(required=True)
    parser_link.add_argument(
        "-b",
        "--base",
        dest="base_repo",
        metavar="<repo-name>",
        type=str,
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
        "--list",
        dest="list_linked_repos",
        action="store_true",
        help="list linked repos of base repo",
    )

    # switch command parser
    parser_switch = subparsers.add_parser(
        "switch", help="command for switching server rails between phoenix & trinity"
    )
    subparsers_switch = parser_switch.add_subparsers(
        title="switch subcommands",
        description="valid switch subcommands",
        help="switch sub-command help",
        dest="switch_subcommand",
    )
    parser_switch_rails = subparsers_switch.add_parser(
        "rails", help="command for switching rails between available repos"
    )
    parser_switch_rails.add_argument(
        "-t",
        "--target",
        dest="switch_rails",
        metavar="<repo-name>",
        type=str,
        choices=[
            "phoenix",
            "trinity",
        ],
        help="a repository name to switch rails frontend repo on server",
    )
    parser_switch_addlings = subparsers_switch.add_parser(
        "addlings", help="command for switching rails between available repos"
    )
    parser_switch_addlings.add_argument(
        "-t",
        "--target",
        dest="switch_addling",
        metavar="<addling_name>",
        type=str,
        choices=[
            "receipt",
            "invoice",
        ],
        help="a addling name to switch rails addlings on server",
    )

    args = parent_parser.parse_args()

    invoker = Invoker()
    receiver = Receiver()

    # main condition for given arguments
    # start
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
    # link
    elif hasattr(args, "subcommand") and args.subcommand == "link":
        if (
            getattr(args, "target_repos", False)
            or getattr(args, "undo_linked_repos", False)
            or getattr(args, "list_linked_repos", False)
        ):
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
    # switch
    elif hasattr(args, "subcommand") and args.subcommand == "switch":
        # switch rails sub-command
        if hasattr(args, "switch_subcommand") and args.switch_subcommand == "rails":
            if getattr(args, "switch_rails", False):
                invoker.do_something_important(
                    SwitchCommand(receiver, target_repo=args.switch_rails)
                )
            else:
                parser_switch.print_help()
        elif hasattr(args, "switch_subcommand") and args.switch_subcommand == "addlings":
            if getattr(args, "switch_addling", False):
                invoker.do_something_important(
                    SwitchCommand(receiver, target_addling=args.switch_addling)
                )
            else:
                parser_switch.print_help()
        else:
            parent_parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
