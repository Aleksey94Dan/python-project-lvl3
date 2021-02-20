### Hexlet tests and linter status:
![Actions Status](https://github.com/Aleksey94Dan/python-project-lvl3//workflows/hexlet-check/badge.svg)
![Python CI](https://github.com/Aleksey94Dan/python-project-lvl3/workflows/Python%20CI/badge.svg?event=push)
[![Maintainability](https://api.codeclimate.com/v1/badges/2863440f6754f8f6819a/maintainability)](https://codeclimate.com/github/Aleksey94Dan/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2863440f6754f8f6819a/test_coverage)](https://codeclimate.com/github/Aleksey94Dan/python-project-lvl3/test_coverage)
[![Build Status](https://travis-ci.org/Aleksey94Dan/python-project-lvl3.svg?branch=main)](https://travis-ci.org/Aleksey94Dan/python-project-lvl3)

# Description

A utility for downloading the specified address from the network. The utility downloads all the resources specified on the page and changes the page so that it starts referring to local versions.

# Requirements

You must have python version 3.6 installed. or higher.
Also you must have pip installed - The Python Package Installer.

# Installation

    pip install -U -i https://test.pypi.org/simple/ aleksey94dan-page-load --extra-index-url https://pypi.org/simple

[![asciicast](https://asciinema.org/a/yeGqzqMxnapSBG02xzb9ZWsfK.svg)](https://asciinema.org/a/yeGqzqMxnapSBG02xzb9ZWsfK)


# Help

    page-loader -h
    usage: page-loader [-h] [-u URL] [-o OUTPUT] [-v {none,info,debug,error}]

    Downloads a page from the network at the specified address and puts it in the
    specified folder

    optional arguments:
    -h, --help            show this help message and exit
    -u URL, --url URL     Enter the correct page address
    -o OUTPUT, --output OUTPUT
                            The directory where to save files
    -v {none,info,debug,error}, --verbosity {none,info,debug,error}
                            Enables verbose mode with logging display

# Application call example

## Download to current directory

    page-loader https://ru.hexlet.io/courses



## Download to designated directory

    page-loader --output example2 https://ru.hexlet.io/courses


## Download with verbose output

    page-loader --output example2 https://ru.hexlet.io/courses -v debug


