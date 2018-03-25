
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
