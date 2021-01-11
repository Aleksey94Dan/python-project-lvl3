# -*- coding: utf-8 -*-

"""Log setup."""

import logging
import logging.config  # noqa: WPS301
import os

import yaml

NAME_OF_CONFIG = 'log_config.yaml'


def absolute_path(path_to_file: str):
    """Return absolute path to file."""
    dirname = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(dirname, path_to_file)


with open(absolute_path(NAME_OF_CONFIG)) as log_file:
    config = yaml.safe_load(log_file.read())
    logging.config.dictConfig(config)


def log_setup(name: str):
    """Declare logger."""
    logger = logging.getLogger(name)
    logger.debug('This is a debug message')
