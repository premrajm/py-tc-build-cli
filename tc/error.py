class ConfigNotFoundException(Exception):
    """Raise if configuration is missing"""
    pass


class BuildConfigNotFoundException(Exception):
    """Raise if configuration is missing"""
    pass


class AuthNotFoundException(Exception):
    """Raise if login configuration is missing"""
    pass


class RequestFailedException(Exception):
    """Raise if request status is other than 200"""
    pass
