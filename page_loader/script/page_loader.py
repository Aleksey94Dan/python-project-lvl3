# !/usr/bin/env python3  # noqa: C101

# -*- coding:utf-8 -*-

"""The main parsing script."""

import sys

from requests import exceptions

from page_loader import cli, loader, logging_app

START = 'Start'
FINISH = 'Finish'
SYSTEM_EXIT_ABORT = 1


def main() -> None:
    """Run a code."""
    logger = logging_app.logger
    path_to_file, url, verbose = cli.parse()

    logger_level = logger.debug if verbose else logger.info
    logger.info(START)
    try:
        loader.download(url, path_to_file)
    except (TypeError, exceptions.MissingSchema, exceptions.InvalidSchema):
        logger_level(
            SystemExit('Please enter correct URL. Exit code {0}.'.format(
                SYSTEM_EXIT_ABORT,
            ),
            ),
        )
        sys.exit(SYSTEM_EXIT_ABORT)
    logger.info('The program ended successfully')
    logger.info(FINISH)


if __name__ == '__main__':
    main()
