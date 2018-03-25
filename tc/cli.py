import base64
import click
import os
import configparser
import tc.utils as utils

class BuildConfig:
    config_file = 'tc-build.ini'
    main = 'Main'
    main_server = 'server'
    main_tag = 'tag'

authConfig = os.environ.get('HOME') + '/.tcbuild/{0}.auth'
build_config = BuildConfig()


@click.group()
def main():
    pass


@main.command()
def status():
    """get the build related info from team city server"""
    click.echo('SUCCESS')


@main.command()
@click.option('--server', prompt='Team city Server', help='team city server host name without port (e.g. localhost)')
@click.option('--username', prompt='Username', help='team city username')
@click.option('--password', prompt='Password', help='team city password', hide_input=True)
def login(server, username, password):
    """configure login credentials for tc server"""
    auth = '{0}:{1}'.format(username, password)
    utils.writeFile(authConfig.format(server), base64.b64encode(auth.encode()).decode('utf-8'))


@main.command()
@click.option('--generate', is_flag=True, help='create/overwrite config file')
def config(generate):
    """configure or print build configuration"""
    if generate:
        _create_build_configuration()
    else:
        _print_build_configuration()


def _print_build_configuration():
    try:
        cfg_file = open(build_config.config_file,'r')
        message = cfg_file.read()
        click.echo(message)
        cfg_file.close()
    except IOError:
        click.echo('No config exists. create with --generate flag')

def _create_build_configuration():
    cfg_file = open(build_config.config_file, 'w')
    config_parser = configparser.ConfigParser()
    config_parser.add_section(build_config.main)
    config_parser.set(build_config.main, build_config.main_server, click.prompt('Please enter server host:port', type=click.STRING))
    config_parser.set(build_config.main, build_config.main_tag, click.prompt('Please enter build tag', type=click.STRING))
    config_parser.write(cfg_file)
    cfg_file.close()

