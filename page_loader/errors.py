# -*- coding:utf-8 -*-

"""The module handles errors."""


class DownloadError(Exception):
    """Exception due to download errors."""

    def __init__(self, message):
        self.message = message


class DownloadNetworkError(DownloadError):
    """Connection error exception."""

    def __init__(self, message):
        self.message = message


class DownloadFileError(DownloadError):
    """File download error."""

    def __init__(self, message):
        self.message = message


class DownloadDirectoryError(DownloadError):
    """Error downloading to directory."""

    def __init__(self, message):
        self.message = message
