# !/usr/bin/env python3  # noqa: C101

# -*- coding:utf-8 -*-

"""The main parsing script."""

import logging

from page_loader import cli, loader

START = 'Start'
FINISH = 'Finish'


def main() -> None:
    """Run a code."""
    path_to_file, url = cli.parse()
    logging.info(START)
    loader.download(url, directory=path_to_file)
    logging.info(FINISH)


if __name__ == '__main__':
    main()
