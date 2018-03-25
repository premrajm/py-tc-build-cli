import base64
import click
import os
import tc.utils as utils

authConfig = os.environ.get('HOME') + '/.tcbuild/{0}.auth'


@click.group()
def main():
    pass


@main.command()
def status():
    """Get the build related info from team city server"""
    click.echo('SUCCESS')


@main.command()
@click.option('--server', prompt='Team city Server', help='team city server host name without port (e.g. localhost)')
@click.option('--username', prompt='Username', help='team city username')
@click.option('--password', prompt='Password', help='team city password', hide_input=True)
def login(server, username, password):
    """configure login credentials for tc server"""
    auth = '{0}:{1}'.format(username, password)
    utils.writeFile(authConfig.format(server), base64.b64encode(auth.encode()).decode('utf-8'))

