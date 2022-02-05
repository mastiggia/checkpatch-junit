# checkpatch-junit

[![Python Version](https://img.shields.io/badge/python-3.x-blue?style=flat&logo=python)](#)
[![OS](https://img.shields.io/badge/OS-GNU%2FLinux-red?style=flat&logo=linux)](#)
[![License](https://img.shields.io/github/license/mastiggia/checkpatch-junit?style=flat&logo=github)](#)
[![PyPI](https://img.shields.io/pypi/v/checkpatch-junit?color=blue)](https://pypi.org/project/checkpatch-junit/)
[![CodeStyle](https://img.shields.io/badge/code%20style-black-000000.svg)](#)

A Python program to generate JUnit XML test result from Linux script
checkpatch.pl output.

Then, this result can be consumed by continuous integration tools
(Jenkins, GitLab CI ...) to provide nice information display.

## Installation

### Install from PyPI

```sh
pip install checkpatch-junit
```

### Clone and install from GitHub

```sh
git clone https://github.com/mastiggia/checkpatch-junit
python setup.py install
```

## Usage

```sh
checkpatch-junit [-h] [-c checkpatch.pl] [--checkpatch-args arg1,arg2,...]
                 [-o outfile.xml] [--ignore-check] [--ignore-warning]
                 FILE [FILE ...]

Provide JUnit output to Linux checkpatch.pl script

positional arguments:
  FILE                  patch to analyze with checkpatch.pl

options:
  -h, --help            show this help message and exit
  -c checkpatch.pl      path to the checkpatch.pl script to use
  --checkpatch-args arg1,arg2,...
                        extra arguments to pass to checkpatch.pl, separated by
                        commas instead of spaces
  -o outfile.xml        output JUnit XML file
  --ignore-check        ignore checkpatch.pl check messages
  --ignore-warning      ignore checkpatch.pl warning messages
```

Basic example:

```sh
checkpatch-junit -c scripts/checkpatch.pl --checkpatch-args=--no-tree *.patch -o checkpatch.xml
```

## CI example

### GitLab

The following screenshot shows a GitLab merge request which fixes 2 patches:

![MergeRequest](https://raw.githubusercontent.com/mastiggia/checkpatch-junit/main/examples/gitlab/merge-request.jpg)
