# !/usr/bin/env python3  # noqa: C101

# -*- coding:utf-8 -*-

"""The main parsing script."""

import logging
import sys

from requests import exceptions

from page_loader import cli, loader

START = 'Start'
FINISH = 'The program ended successfully'
SYSTEM_EXIT_ABORT = 1
SYSTEM_EXIT_GOOD = 0


def main() -> None:  # noqa: WPS210
    """Run a code."""
    path_to_file, url, verbose = cli.parse()
    logger_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',  # noqa: WPS323
        level=logger_level,
    )
    logger = logging.getLogger(__name__)
    logger.info(START)
    exit_code = SYSTEM_EXIT_GOOD
    try:
        loader.download(url, path_to_file)
    except (TypeError, exceptions.MissingSchema, exceptions.InvalidSchema):
        logger.error(
            SystemExit('Please enter correct URL. Exit code {0}.'.format(
                SYSTEM_EXIT_ABORT,
            ),
            ),
        )
        exit_code = SYSTEM_EXIT_ABORT
    sys.exit(exit_code)
    logger.info(FINISH)


if __name__ == '__main__':
    main()
