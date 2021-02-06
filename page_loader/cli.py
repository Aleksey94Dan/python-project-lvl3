# -*- coding:utf-8 -*-

"""Extraction of urls and directories from the command line."""
import argparse
import os


def dir_path(path):
    """Check if the specified directory exists."""
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(
        '{0} is not valid path'.format(path),
    )


def parse():
    """Parser command line arguments."""
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description=(
            'Downloads a page from the network at the specified '
            'address and puts it in the specified folder'  # noqa: WPS326
        ),
    )
    parser.add_argument(
        '-O',
        '--output',
        type=dir_path,
        default=os.getcwd(),
        help='The directory where to save files',
    )
    parser.add_argument(
        '-u',
        '--url',
        type=str,
        help='Enter the correct page address',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enables verbose mode with logging display',
    )
    args = parser.parse_args()
    return args.output, args.url, args.verbose
