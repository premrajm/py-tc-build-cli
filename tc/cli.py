import click
import os
import configparser
import tc.utils as utils

class BuildConfig:
    config_file = 'tc-build.ini'
    main = 'Main'
    main_server = 'server'
    main_tag = 'tag'


class AuthConfig:
    config_file = os.environ.get('HOME') + '/.tcbuild/{0}.auth'
    auth = 'Auth'
    auth_user = 'user'
    auth_pass = 'password'


class ConfigNotFoundException(Exception):
    """Raise if build configuration is missing"""
    pass


build_config = BuildConfig()
auth_config = AuthConfig()


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
    config_parser = configparser.ConfigParser()
    config_parser.add_section(auth_config.auth)
    config_parser.set(auth_config.auth, auth_config.auth_user, username)
    config_parser.set(auth_config.auth, auth_config.auth_pass, password)
    _write_config(auth_config.config_file.format(server), config_parser)


@main.command()
@click.option('--generate', is_flag=True, help='create/overwrite config file')
def config(generate):
    """configure or print build configuration"""
    if generate:
        _create_build_configuration()
    else:
        try:
            _print_build_configuration()
        except ConfigNotFoundException:
            click.echo('No config exists. create with --generate flag')


def _print_build_configuration():
    try:
        cfg_file = open(build_config.config_file,'r')
        message = cfg_file.read()
        click.echo(message)
        cfg_file.close()
    except IOError:
        raise ConfigNotFoundException()


def _create_build_configuration():
    config_parser = configparser.ConfigParser()
    config_parser.add_section(build_config.main)
    config_parser.set(build_config.main, build_config.main_server, click.prompt('Please enter server host:port', type=click.STRING))
    config_parser.set(build_config.main, build_config.main_tag, click.prompt('Please enter build tag', type=click.STRING))
    _write_config(build_config.config_file, config_parser)

def _write_config(filename, config_parser):
    cfg_file = utils.create_and_open(filename, 'w')
    config_parser.write(cfg_file)
    cfg_file.close()


