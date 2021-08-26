import argparse
import sys

from parasut_cli.utils.invoker import Invoker
from parasut_cli.utils.receiver import Receiver
from parasut_cli.commands.start import StartCommand
from parasut_cli.commands.link import LinkCommand
from parasut_cli.commands.switch import SwitchCommand
from parasut_cli.commands.run import RunCommand
from parasut_cli.commands.release import ReleaseCommand
from parasut_cli.commands.version import VersionCommand


def main():
    parent_parser = argparse.ArgumentParser("Parasut CLI")
    subparsers = parent_parser.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="sub-command help",
        dest="subcommand",
    )

    # version argument
    parent_parser.add_argument(
        "-v",
        "--version",
        dest="version_pkg",
        action="store_true",
        help="version of the package",
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
            "post-office",
            "ubl-validator",
        ],
        help="a repository name to open in text editor",
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
            "post-office",
            "ubl-validator",
        ],
        help="a repository name to launch",
    )
    parser_start.add_argument(
        "-w",
        "--worker",
        dest="workers",
        metavar="<worker-name>",
        type=str,
        nargs="+",
        choices=[
            "server-worker",
            "e-doc-broker-worker",
        ],
        help="a worker name to launch",
    )

    # link command parser
    parser_link = subparsers.add_parser("link", help="command for linking")
    group_parser_link = parser_link.add_mutually_exclusive_group(required=True)
    parser_link.add_argument(
        "-b",
        "--base",
        dest="base_repo",
        metavar="<repo-name>",
        type=str,
        choices=["phoenix", "trinity"],
        required=True,
        help="a base repository name for linking target repository.",
    )
    group_parser_link.add_argument(
        "-t",
        "--target",
        dest="target_repos",
        metavar="<repo-name>",
        type=str,
        nargs="+",
        choices=["ui-library", "shared-logic"],
        help="a target repository name for linking it to base repository",
    )
    group_parser_link.add_argument(
        "-u",
        "--undo",
        dest="undo_linked_repos",
        metavar="<repo-name>",
        type=str,
        nargs="+",
        choices=["ui-library", "shared-logic"],
        help="a repository name for unlinking",
    )
    group_parser_link.add_argument(
        "--list",
        dest="list_linked_repos",
        action="store_true",
        help="list linked repos of base repo",
    )
    parser_link.add_argument(
        "--output",
        dest="show_output_link",
        action="store_true",
        help="show output of linking action",
    )

    # switch command parser
    parser_switch = subparsers.add_parser(
        "switch", help="command for switching on server side."
    )
    subparsers_switch = parser_switch.add_subparsers(
        title="switch subcommands",
        description="valid switch subcommands",
        help="switch sub-command help",
        dest="switch_subcommand",
    )
    subparser_switch_frontend = subparsers_switch.add_parser(
        "frontend", help="command for switching frontend between available repos"
    )
    subparser_switch_frontend.add_argument(
        "-t",
        "--target",
        dest="switch_frontend",
        metavar="<repo-name>",
        type=str,
        choices=[
            "phoenix",
            "trinity",
        ],
        required=True,
        help="a repository name to switch frontend repo on server",
    )
    subparser_switch_frontend.add_argument(
        "--output",
        dest="show_output_frontend",
        action="store_true",
        help="show output of switch frontend action",
    )
    subparser_switch_addlings = subparsers_switch.add_parser(
        "addlings", help="command for switching addlings"
    )
    subparser_switch_addlings.add_argument(
        "-t",
        "--target",
        dest="switch_addling",
        metavar="<addling_name>",
        type=str,
        choices=[
            "receipt",
            "invoice",
        ],
        required=True,
        help="a addling name to switch addlings on server",
    )
    subparser_switch_addlings.add_argument(
        "--output",
        dest="show_output_addlings",
        action="store_true",
        help="show output of switch addling action",
    )
    subparser_switch_pricing_list = subparsers_switch.add_parser(
        "pricing_list", help="command for switching pricing list"
    )
    subparser_switch_pricing_list.add_argument(
        "-t",
        "--target",
        dest="switch_pricing_list",
        metavar="<pricing_list_name>",
        type=str,
        choices=[
            "phoenix",
            "trinity",
        ],
        required=True,
        help="a name to switch pricing list on billing",
    )
    subparser_switch_pricing_list.add_argument(
        "--output",
        dest="show_output_pricing_list",
        action="store_true",
        help="show output of switch pricing list action",
    )

    # run command parser
    parser_run = subparsers.add_parser(
        "run", help="command for running repo with necessary options"
    )
    parser_run.add_argument(
        "-t",
        "--target",
        dest="run_repo",
        metavar="<repo-name>",
        type=str,
        choices=[
            "server",
            "server-sidekiq",
            "billing",
            "billing-sidekiq",
            "e-doc-broker",
            "e-doc-broker-sidekiq",
            "post-office",
            "post-office-sidekiq",
            "ubl-validator",
            "phoenix",
            "shared-logic",
            "trinity",
            "ui-library",
            "client",
        ],
        required=True,
        help="a repository name",
    )

    # release command parser
    parser_release = subparsers.add_parser("release", help="command for release")
    parser_release.add_argument(
        "-t",
        "--target",
        dest="release_repo",
        metavar="<repo-name>",
        type=str,
        choices=[
            "shared-logic",
            "ui-library",
        ],
        required=True,
        help="a repository name for releasing",
    )
    parser_release.add_argument(
        "--auto-login",
        dest="auto_login_release",
        action="store_true",
        help="releasing without entering username&password",
    )
    parser_release.add_argument(
        "--output",
        dest="show_output_release",
        action="store_true",
        help="show output of release action",
    )

    args = parent_parser.parse_args()

    invoker = Invoker()
    receiver = Receiver()

    # main condition for given arguments
    # bare arguments
    if getattr(args, "subcommand") == None:
        # version
        if getattr(args, "version_pkg", False):
            invoker.do_something_important(
                VersionCommand(
                    receiver,
                )
            )
        else:
            parent_parser.print_help()
    # start
    elif hasattr(args, "subcommand") and args.subcommand == "start":
        if (
            getattr(args, "edit_repos", False)
            or getattr(args, "setup_repos", False)
            or getattr(args, "workers", False)
        ):
            invoker.do_something_important(
                StartCommand(
                    receiver,
                    setup_repos=args.setup_repos,
                    edit_repos=args.edit_repos,
                    workers=args.workers,
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
                    show_output=args.show_output_link,
                )
            )
        else:
            parser_link.print_help()
    # switch
    elif hasattr(args, "subcommand") and args.subcommand == "switch":
        # switch_frontend sub-command
        if hasattr(args, "switch_subcommand") and args.switch_subcommand == "frontend":
            if getattr(args, "switch_frontend", False):
                invoker.do_something_important(
                    SwitchCommand(
                        receiver,
                        target_repo=args.switch_frontend,
                        show_output=args.show_output_frontend,
                    )
                )
            else:
                subparser_switch_frontend.print_help()
        # switch_addlings sub-command
        elif (
            hasattr(args, "switch_subcommand") and args.switch_subcommand == "addlings"
        ):
            if getattr(args, "switch_addling", False):
                invoker.do_something_important(
                    SwitchCommand(
                        receiver,
                        target_addling=args.switch_addling,
                        show_output=args.show_output_addlings,
                    )
                )
            else:
                subparser_switch_addlings.print_help()
        # switch_pricing_list sub-command
        elif (
            hasattr(args, "switch_subcommand") and args.switch_subcommand == "pricing_list"
        ):
            if getattr(args, "switch_pricing_list", False):
                invoker.do_something_important(
                    SwitchCommand(
                        receiver,
                        target_pricing_list=args.switch_pricing_list,
                        show_output=args.show_output_pricing_list,
                    )
                )
            else:
                subparser_switch_addlings.print_help()
        else:
            parser_switch.print_help()
    # run
    elif hasattr(args, "subcommand") and args.subcommand == "run":
        if getattr(args, "run_repo", False):
            invoker.do_something_important(
                RunCommand(
                    receiver,
                    repo_name=args.run_repo,
                )
            )
        else:
            parser_run.print_help()
    # release
    elif hasattr(args, "subcommand") and args.subcommand == "release":
        if getattr(args, "release_repo", False):
            invoker.do_something_important(
                ReleaseCommand(
                    receiver,
                    target_repo=args.release_repo,
                    auto_login=args.auto_login_release,
                    show_output=args.show_output_release,
                )
            )
        else:
            parser_release.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
