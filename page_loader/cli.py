# -*- coding:utf-8 -*-

"""Extraction of urls and directories from the command line."""
import argparse
import os
from page_loader import loader


def compose(g, f):
    def inner(arg):
        return g(f(arg))
    return inner

get_default_directory = compose(os.path.abspath, os.getcwd)
get_type_directory = os.path.abspath

def parse():
    """Parser command line arguments."""
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description=(
            'Downloads a page from the network at the specified '
            'address and puts it in the specified folder',
        ),
    )
    parser.add_argument(
        '-O',
        '--output',
        default=get_default_directory,
        type=get_type_directory,
        help='set directory of saving',
    )
    parser.add_argument(
        'url',
        help='enter url',
    )
    args = parser.parse_args()
    return (
        args.output,
        args.url,
    )
