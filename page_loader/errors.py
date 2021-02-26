# -*- coding:utf-8 -*-

"""The module handles errors."""


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
