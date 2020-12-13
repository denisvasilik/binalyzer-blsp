"""
    binalyzer_blsp.cli
    ~~~~~~~~~~~~~~~~~~

    CLI extension for the *binalyzer* command.
"""
import click
import socketserver

from .blsp import (
    BLSPServer,
    logger,
)


def show_server_banner(host, port):
    """Show extra startup messages the first time the server is run.
    """
    logger.info(f'BLSP Server running at {host}:{port}')


@click.command()
@click.option('--host', '-h', default='0.0.0.0', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, help='The port to bind to.')
def blsp(host, port):
    """Run a local BLSP server.
    """
    show_server_banner(host, port)

    with socketserver.TCPServer((host, port), BLSPServer) as blsp_server:
        blsp_server.serve_forever()
