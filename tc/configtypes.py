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
