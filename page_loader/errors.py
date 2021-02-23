# -*- coding:utf-8 -*-

"""The module handles errors."""


class DownloadError(Exception):
    """Exception due to download errors."""

    def __init__(self, expression, message):
        """Initializate of starting accepted values."""
        self.expression = expression
        self.message = message


class DownloadNetworkError(DownloadError):
    """Connection error exception."""

    def __init__(self, expression, message):
        """Initializate of starting accepted values."""
        self.expression = expression
        self.message = message
