# !/usr/bin/env python3  # noqa: C101

# -*- coding:utf-8 -*-

"""The main parsing script."""

from page_loader import cli, loader


def main() -> None:
    """Run a code."""
    path_to_file, url = cli.parse()
    loader.load(url, path_to_file)


if __name__ == '__main__':
    main()
