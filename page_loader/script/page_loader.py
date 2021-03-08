# !/usr/bin/env python3  # noqa: C101

# -*- coding:utf-8 -*-

"""The main parsing script."""
import logging
import sys

from page_loader import cli, errors, loader, my_logging

EXIT_SUCCES = 0
EXIT_FAILURE = 1


def main() -> None:  # noqa: WPS210
    """Run a code."""
    try:  # noqa: WPS229
        args = cli.get_parser().parse_args()
        url = args.url
        output = args.output
        level = args.verbosity

        my_logging.setup(level)
        logging.debug(
            'The following arguments were introduced: {0}'.format(args),
        )

        exit_code = EXIT_SUCCES
        loader.download(url, output)
    except SystemExit as mistake1:
        exit_code = mistake1.code
    except errors.DownloadError as mistake2:
        logging.debug(
            str(mistake2.__cause__),  # noqa: WPS609
            exc_info=True,
        )
        logging.error(mistake2.message)
        exit_code = EXIT_FAILURE
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
