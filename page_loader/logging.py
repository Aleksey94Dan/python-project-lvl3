# -*- coding:utf-8 -*-

"""Basic logging setup."""

import logging
from typing import Optional

NONE = 'none'
DEBUG = 'debug'
INFO = 'info'
ERROR = 'error'


def setup(level: Optional[str]):
    """Configure a basic logger."""
    if level == INFO:
        log_level = logging.INFO
    elif level == DEBUG:
        log_level = logging.DEBUG
    elif level == ERROR:
        log_level = logging.ERROR

    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
    )
    chanel = logging.StreamHandler()
    chanel.setFormatter(formatter)
    logger.addHandler(chanel)
