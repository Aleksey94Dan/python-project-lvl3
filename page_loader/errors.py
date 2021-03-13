# -*- coding:utf-8 -*-

"""The module handles errors."""


class DownloadError(Exception):
    """Exception due to download errors."""

    def __init__(self, message):
        """Initialize message of download error."""
        self.message = message


class DownloadNetworkError(DownloadError):
    """Connection error exception."""

    def __init__(self, message):
        """Initialize message of connection error."""
        self.message = message


class DownloadFileError(DownloadError):
    """File download error."""

    def __init__(self, message):
        """Initialize message of donwload file error."""
        self.message = message


class DownloadDirectoryError(DownloadError):
    """Error downloading to directory."""

    def __init__(self, message):
        """Initialize message of donwload error to directory."""
        self.message = message
