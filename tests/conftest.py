#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path

import pytest

CHECKPATH_TESTS_PATH = "tests"

CHECKPATH_TESTS_DATA_PATH = os.path.join(CHECKPATH_TESTS_PATH, "data")

CHECKPATCH_DATA = {
    "0001-ath11k-add-support-of-firmware-logging-for-WCN6855.patch": {
        "ERROR": 0,
        "WARNING": 1,
        "CHECK": 3,
    },
    "0001-ath5k-switch-to-rate-table-based-lookup.patch": {
        "ERROR": 1,
        "WARNING": 0,
        "CHECK": 0,
    },
    "0001-drm-amdgpu-add-support-for-IP-discovery-gc_info-tabl.patch": {
        "ERROR": 0,
        "WARNING": 8,
        "CHECK": 0,
    },
    "0001-iwlwifi-mei-wait-before-mapping-the-shared-area.patch": {
        "ERROR": 0,
        "WARNING": 2,
        "CHECK": 0,
    },
    "0001-libbpf-Use-100-character-limit-to-make-bpf_tracing.h.patch": {
        "ERROR": 15,
        "WARNING": 0,
        "CHECK": 0,
    },
    "0001-net-ena-Add-debug-prints-for-invalid-req_id-resets.patch": {
        "ERROR": 0,
        "WARNING": 0,
        "CHECK": 0,
    },
    "0001-net-mlx5e-Expose-FEC-counters-via-ethtool.patch": {
        "ERROR": 0,
        "WARNING": 0,
        "CHECK": 1,
    },
    "0001-net-wan-lmc-fix-spelling-of-its.patch": {
        "ERROR": 1,
        "WARNING": 3,
        "CHECK": 1,
    },
}


def pytest_generate_tests(metafunc):
    # checkpatch.pl provides different results depending if the patch file
    # is under a git repository or not (why?)
    # To avoid that, overwrite the GIT_DIR environment variable before running
    # the tests
    os.environ["GIT_DIR"] = ""


@pytest.fixture
def checkpatch_script():
    return os.path.join(CHECKPATH_TESTS_PATH, "checkpatch.pl")


@pytest.fixture
def all_patches():
    return [
        os.path.join(CHECKPATH_TESTS_DATA_PATH, patch)
        for patch in CHECKPATCH_DATA.items()
    ]


@pytest.fixture
def patches_only_errors():
    return [
        os.path.join(CHECKPATH_TESTS_DATA_PATH, patch)
        for patch, result in CHECKPATCH_DATA.items()
        if result["ERROR"] != 0
        and result["WARNING"] == 0
        and result["CHECK"] == 0
    ]


@pytest.fixture
def patches_only_warnings():
    return [
        os.path.join(CHECKPATH_TESTS_DATA_PATH, patch)
        for patch, result in CHECKPATCH_DATA.items()
        if result["ERROR"] == 0
        and result["WARNING"] != 0
        and result["CHECK"] == 0
    ]


@pytest.fixture
def patches_only_checks():
    return [
        os.path.join(CHECKPATH_TESTS_DATA_PATH, patch)
        for patch, result in CHECKPATCH_DATA.items()
        if result["ERROR"] == 0
        and result["WARNING"] == 0
        and result["CHECK"] != 0
    ]


@pytest.fixture
def patches_with_errors():
    return [
        os.path.join(CHECKPATH_TESTS_DATA_PATH, patch)
        for patch, result in CHECKPATCH_DATA.items()
        if sum(result.values()) != 0
    ]


@pytest.fixture
def patches_without_error():
    return [
        os.path.join(CHECKPATH_TESTS_DATA_PATH, patch)
        for patch, result in CHECKPATCH_DATA.items()
        if sum(result.values()) == 0
    ]
