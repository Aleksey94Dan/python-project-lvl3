# -*- coding:utf-8 -*-

"""The module handles errors."""
from functools import wraps
import logging
class DownloadError(Exception):
    """Exception due to download errors."""

    def __init__(self, message):
        """Initializate of starting accepted values."""
        self.message = message


class DownloadNetworkError(DownloadError):
    """Connection error exception."""

    def __init__(self, message):
        """Initializate of starting accepted values."""
        self.message = message


class DownloadFileError(DownloadError):
    """Connection error exception."""

    def __init__(self, message):
        """Initializate of starting accepted values."""
        self.message = message


class DownloadDirectoryError(DownloadError):
    """"""

    def __init__(self, message):
        """Initializate of starting accepted values."""
        self.message = message


class Supress:

    def __init__(self, exception):
        self.exception = exception

    def __call__(self, function):
        @wraps(function)
        def wrapper(url, out):
            try:
                return function(url, out)
            except self.exception as err:
                logging.debug(str(err.__cause__), exc_info=True)
                logging.error(err.message)
        return wrapper