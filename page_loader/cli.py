# -*- coding:utf-8 -*-

"""Extraction of urls and directories from the command line."""

import argparse
import os

from page_loader import logging


def dir_path(path: str) -> str:
    """Check if the specified directory exists."""
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            '{0} is not valid path'.format(path),
        )
    return path


def get_parser() -> argparse.ArgumentParser:
    """Parser command line arguments."""
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description=(
            'Downloads a page from the network at the specified '
            'address and puts it in the specified folder'  # noqa: WPS326
        ),
    )
    parser.add_argument(
        '-u',
        '--url',
        type=str,
        help='Enter the correct page address',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=dir_path,
        default=os.getcwd(),
        help='The directory where to save files',
    )
    parser.add_argument(
        '-v',
        '--verbosity',
        action='store',
        default=logging.NONE,
        type=str,
        help='Enables verbose mode with logging display',
        choices=[
            logging.NONE,
            logging.INFO,
            logging.DEBUG,
            logging.ERROR,
        ],
    )
    return parser
