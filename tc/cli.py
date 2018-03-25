import click
import configparser
import os


class BuildConfig:
    config_file = 'tc-build.ini'
    main = 'Main'
    main_server = 'server'
    main_type_id = 'type_id'


class AuthConfig:
    config_file = os.environ.get('HOME') + '/.tcbuild/{0}.auth'
    auth = 'Auth'
    auth_user = 'user'
    auth_pass = 'password'


class ConfigNotFoundException(Exception):
    """Raise if configuration is missing"""
    pass


class BuildConfigNotFoundException(Exception):
    """Raise if configuration is missing"""
    pass


class AuthNotFoundException(Exception):
    """Raise if login configuration is missing"""
    pass


class AuthenticationException(Exception):
    """Raise if login failed"""
    pass


build_config = BuildConfig()
auth_config = AuthConfig()


@click.group()
def main():
    pass


@main.command()
def status():
    """get the build related info from team city server"""
    try:
        config_parser = _get_build_config_parser()
        server = config_parser.get(build_config.main, build_config.main_server)
        build_type_id = config_parser.get(build_config.main, build_config.main_type_id)
        build_status = _build_status(server, build_type_id)
        click.echo(build_status)
    except BuildConfigNotFoundException:
        click.echo('Build config missing. Create with "config --generate" command')
    except AuthNotFoundException:
        click.echo('Login config missing. Create with "login" command')


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
            click.echo('No config exists. Create with --generate flag')


def _print_build_configuration():
    try:
        cfg_file = open(build_config.config_file, 'r')
        message = cfg_file.read()
        click.echo(message)
        cfg_file.close()
    except IOError:
        raise ConfigNotFoundException()


def _create_build_configuration():
    config_parser = configparser.ConfigParser()
    config_parser.add_section(build_config.main)
    config_parser.set(build_config.main, build_config.main_server,
                      click.prompt('Please enter server host:port', type=click.STRING))
    config_parser.set(build_config.main, build_config.main_type_id,
                      click.prompt('Please enter build tag', type=click.STRING))
    _write_config(build_config.config_file, config_parser)


def _write_config(filename, config_parser):
    cfg_file = create_and_open(filename, 'w')
    config_parser.write(cfg_file)
    cfg_file.close()


def _get_config_parser(filename):
    config_parser = configparser.ConfigParser()
    file_read = config_parser.read(filename)
    if len(file_read) == 0:
        raise ConfigNotFoundException()
    return config_parser


def _get_build_config_parser():
    try:
        return _get_config_parser(build_config.config_file)
    except ConfigNotFoundException:
        raise BuildConfigNotFoundException()


def _get_auth_config_parser(server):
    try:
        return _get_config_parser(auth_config.config_file.format(server.split(':')[0]))
    except ConfigNotFoundException:
        raise AuthNotFoundException()


def _build_status(server, build_type_id):
    auth_config_parser = _get_auth_config_parser(server)
    build_url = 'http://{0}/httpAuth/app/rest/builds/buildType:{1}/status'.format(server, build_type_id)
    username = auth_config_parser.get(auth_config.auth, auth_config.auth_user)
    password = auth_config_parser.get(auth_config.auth, auth_config.auth_pass)
    return 'SUCCESS'


def create_and_open(filename, mode):
    if "/" in filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    return open(filename, mode)
