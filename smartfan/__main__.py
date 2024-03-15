import sys
from argparse import ArgumentParser
from smartfan.cli.run import define_argparser as def_run
from smartfan.connection.client import define_argparser as def_client
from smartfan.connection.server import define_argparser as def_server


def define_argparser() -> ArgumentParser:
    cli_parser = ArgumentParser(
        prog="smartfan",
        description="Smart, low power climate control system.")

    command_parser = cli_parser.add_subparsers(
        title="commands",
        dest="command",
        required=True)

    def_run(command_parser)
    def_server(command_parser)
    def_client(command_parser)

    return cli_parser


def main() -> None:
    args = define_argparser().parse_args()
    exit_code = args.handler(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()