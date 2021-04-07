### Hexlet tests and linter status:
[![hexlet-check](https://github.com/Aleksey94Dan/python-project-lvl3/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Aleksey94Dan/python-project-lvl3/actions/workflows/hexlet-check.yml)
[![Python CI](https://github.com/Aleksey94Dan/python-project-lvl3/actions/workflows/CI.yml/badge.svg)](https://github.com/Aleksey94Dan/python-project-lvl3/actions/workflows/CI.yml)
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

[![asciicast](https://asciinema.org/a/A49DNS73dDzROGy622xSyv9RA.svg)](https://asciinema.org/a/A49DNS73dDzROGy622xSyv9RA)
# Help

    page-loader -h
    usage: page-loader [-h] [-o OUTPUT] [-v {none,info,debug,error}] url

    Downloads a page from the network at the specified address and puts it in the
    specified folder

    positional arguments:
    url                   Enter the correct page address

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                          The directory where to save files
    -v {none,info,debug,error}, --verbosity {none,info,debug,error}
                          Enables verbose mode with logging displa

# Application call example

## Download to current directory

    page-loader https://page-loader.hexlet.repl.co/

[![asciicast](https://asciinema.org/a/bVCQzYJdN2d7Y7hfxgLxwAMh5.svg)](https://asciinema.org/a/bVCQzYJdN2d7Y7hfxgLxwAMh5)
## Download to designated directory

    page-loader -o demo/ https://page-loader.hexlet.repl.co/

[![asciicast](https://asciinema.org/a/9eBIX2xYDgFpIoqqgohlc3x1J.svg)](https://asciinema.org/a/9eBIX2xYDgFpIoqqgohlc3x1J)

## Download with verbose output

    page-loader -o demo/ https://page-loader.hexlet.repl.co/ -v debug

[![asciicast](https://asciinema.org/a/NTQwDXAQ3MDBZDQLTjMA5a3BQ.svg)](https://asciinema.org/a/NTQwDXAQ3MDBZDQLTjMA5a3BQ)
