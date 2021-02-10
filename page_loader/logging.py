# -*- coding:utf-8 -*-

import logging
from typing import Optional

LOG_LEVEL = (
    NONE,
    DEBUG,
    INFO,
    ERROR,
) = 'none', 'debug', 'info', 'error'


def setup(level: Optional[str]):
    """Configure a basic logger."""
    if level == NONE:
        log_level = None
    elif level == INFO:
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
