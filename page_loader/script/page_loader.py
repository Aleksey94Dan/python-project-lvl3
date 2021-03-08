# !/usr/bin/env python3
# -*- coding:utf-8 -*-

"""The main parsing script."""

import logging
import sys

from page_loader import cli, errors, loader, my_logging

EXIT_SUCCES = 0
EXIT_FAILURE = 1


def main() -> None:  # noqa: WPS210, WPS213
    """Run a code."""
    args = cli.get_parser().parse_args()
    url = args.url
    output = args.output
    level = args.verbosity

    my_logging.setup(level)
    logging.debug(
        'The following arguments were introduced: {0}'.format(args),
    )
    exit_code = EXIT_FAILURE
    try:  # noqa: WPS225, WPS229
        loader.download(url, output)
        exit_code = EXIT_SUCCES
    except errors.DownloadDirectoryError as err1:
        logging.debug(
            str(err1.__cause__),  # noqa: WPS609
            exc_info=True,
        )
        logging.error(err1.message)
    except errors.DownloadFileError as err2:
        logging.debug(
            str(err2.__cause__),  # noqa: WPS609
            exc_info=True,
        )
        logging.error(err2.message)
    except errors.DownloadNetworkError as err3:
        logging.debug(
            str(err3.__cause__),  # noqa: WPS609
            exc_info=True,
        )
        logging.error(err3.message)
    except errors.DownloadFileError as err4:
        logging.debug(
            str(err4.__cause__),  # noqa: WPS609
            exc_info=True,
        )
        logging.error(err4.message)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
