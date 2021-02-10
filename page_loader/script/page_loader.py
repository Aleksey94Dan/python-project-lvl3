# !/usr/bin/env python3  # noqa: C101

# -*- coding:utf-8 -*-

"""The main parsing script."""

import logging
import sys

from page_loader import cli
from page_loader import loader
from page_loader import logging as my_logging

ABORT_CODE = 1
OK_CODE = 0


def main() -> None:  # noqa: WPS210
    """Run a code."""
    args = cli.get_parser().parse_args()


if __name__ == '__main__':
    main()
