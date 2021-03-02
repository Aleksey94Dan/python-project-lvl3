# -*- coding:utf-8 -*-

"""The module handles errors."""

import logging
from functools import wraps


class DownloadError(Exception):
    """Exception due to download errors."""


class DownloadNetworkError(DownloadError):
    """Connection error exception."""


class DownloadFileError(DownloadError):
    """File download error."""


class DownloadDirectoryError(DownloadError):
    """Error downloading to directory."""


class Supress(object):
    """Suppress exceptions and write to the log."""

    def __init__(self, exception):
        """Initializate of starting accepted values."""
        self.exception = exception

    def __call__(self, function):
        """Call the class as functions."""
        @wraps(function)  # noqa: WPS430
        def wrapper(url, out):
            try:
                return function(url, out)
            except self.exception as mistake:
                logging.debug(
                    str(mistake.__cause__),  # noqa: WPS609
                    exc_info=True,
                )
                logging.error(mistake.message)
        return wrapper
