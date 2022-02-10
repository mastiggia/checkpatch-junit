#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from checkpatch_junit import main


@pytest.fixture
def argv(checkpatch_script):
    return [
        "-c",
        checkpatch_script,
        "--checkpatch-args=--no-tree",
        "-o",
        "/dev/null",
    ]


def test_with_errors(argv, patches_with_errors):
    assert main(argv + patches_with_errors) is True


def test_without_error(argv, patches_without_error):
    assert main(argv + patches_without_error) is False


def test_only_warnings(argv, patches_only_warnings):
    assert main(argv + patches_only_warnings) is True
    assert main(argv + ["--ignore-warning"] + patches_only_warnings) is False


def test_only_checks(argv, patches_only_checks):
    assert main(argv + patches_only_checks) is True
    assert main(argv + ["--ignore-check"] + patches_only_checks) is False
