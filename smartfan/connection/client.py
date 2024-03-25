import socket
from argparse import _SubParsersAction

def define_argparser(command_parser: _SubParsersAction):
    """
    Define `client` subcommand.
    """
    p = command_parser.add_parser(
        'client', help='initiate client connection')

    p.set_defaults(handler=lambda args: start_client())

def start_client():
    HOST = '192.168.1.161'    # The remote host
    PORT = 50007              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        output = bytes(input(), 'utf-8');
        s.sendall(output)
        data = s.recv(1024)
    print('Received', repr(data))