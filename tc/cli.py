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
def login():
    """configure login credentials for tc server"""
    server = click.prompt('Please enter server host name [without port e.g localhost]', type=click.STRING)
    username = click.prompt('Please enter username', type=click.STRING)
    password = click.prompt('Please enter password', type=click.STRING, hide_input=True)
    auth = '{0}:{1}'.format(username, password)
    utils.writeFile(authConfig.format(server), base64.b64encode(auth.encode()).decode('utf-8'))

