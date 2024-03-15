from smartfan.app.gui import SmartFanApp
from argparse import _SubParsersAction

def define_argparser(command_parser: _SubParsersAction):
    """
    Define `run` subcommand.
    """
    p = command_parser.add_parser(
        'run', help='run smartfan app')

    p.set_defaults(handler=lambda args: run())

def run():
    app = SmartFanApp()
    app.run()
