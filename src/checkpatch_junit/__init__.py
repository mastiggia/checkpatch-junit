#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os.path
import re
import subprocess
import sys

import junit_xml


def validate_patch(path):
    """
    Validate a patch file passed as program input
    """
    if not os.path.isfile(path):
        msg = f"unable to find the file '{path}'"
        raise argparse.ArgumentTypeError(msg)
    return path


def validate_checkpatch(path):
    """
    Validate the checkpatch script passed as program input
    """
    if not os.path.isfile(path):
        msg = f"unable to find the file '{path}'"
        raise argparse.ArgumentTypeError(msg)
    if not os.access(path, os.X_OK):
        msg = f"the file '{path}' is not exectutable"
        raise argparse.ArgumentTypeError(msg)
    return path


def validate_checkpatch_args(args):
    """
    Validate checkpatch arguments passed as program input
    """
    return args.split(",")


def run_checkpatch(patch, checkpatch, checkpatch_args):
    """
    Execute the checkpatch.pl script and capture its output
    """
    checkpatch_command = [
        checkpatch,
        "--terse",
        *checkpatch_args,
        patch,
    ]
    with subprocess.Popen(
        checkpatch_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as process:
        stdout, _ = process.communicate()
    return stdout.decode("utf-8")


def filter_checkpatch_output(output, ignore_warning, ignore_check):
    """
    Filter "checkpatch --terse" output
    """
    regex = re.compile(
        r"(?P<filename>[^:]+):"
        r"(?P<line>\d+): "
        r"(?P<msg_type>ERROR|WARNING|CHECK): "
        r"(?P<msg>.+)\n?"
    )
    filtered_output = []
    for line in output.splitlines():
        match = re.match(regex, line)
        if match:
            msg_type = match.group("msg_type")
            if msg_type == "WARNING" and ignore_warning:
                continue
            if msg_type == "CHECK" and ignore_check:
                continue
            filtered_output.append(line)
    return " ".join(filtered_output), len(filtered_output)


def patch_to_test_case(
    patch, checkpatch, checkpatch_args, ignore_warning, ignore_check
):
    """
    Create a JUnit test case with checkpatch.pl result for a patch
    """
    output = run_checkpatch(patch, checkpatch, checkpatch_args)
    filtered_output, errors = filter_checkpatch_output(
        output, ignore_warning, ignore_check
    )
    patch_basename = os.path.basename(patch)
    test_case = junit_xml.TestCase(
        name=patch_basename,
        classname=patch_basename,
        file=patch,
    )
    if errors != 0:
        test_case.add_failure_info(message=filtered_output)
    return test_case, errors


def checkpatch_to_junit(args):
    """
    Create a JUnit report with the result of all patches analysis with
    checkpatch.pl
    """
    test_cases = []
    total_errors = 0
    for patch in args.patches:
        test_case, errors = patch_to_test_case(
            patch,
            args.checkpatch,
            args.checkpatch_args,
            args.ignore_warning,
            args.ignore_check,
        )
        test_cases.append(test_case)
        total_errors += errors
    test_suite = junit_xml.TestSuite("checkpatch", test_cases)
    with args.outfile as outfile:
        outfile.write(junit_xml.TestSuite.to_xml_string([test_suite]))
    sys.exit(total_errors != 0)


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        prog="checkpatch-junit",
        description="Provide JUnit output to Linux checkpatch.pl script",
    )
    parser.add_argument(
        nargs="+",
        default=[],
        type=validate_patch,
        help="patch to analyze with checkpatch.pl",
        metavar="FILE",
        dest="patches",
    )
    parser.add_argument(
        "-c",
        default="scripts/checkpatch.pl",
        type=validate_checkpatch,
        help="path to the checkpatch.pl script to use",
        metavar="checkpatch.pl",
        dest="checkpatch",
    )
    parser.add_argument(
        "--checkpatch-args",
        default="",
        type=validate_checkpatch_args,
        help="extra arguments to pass to checkpatch.pl,"
        " separated by commas instead of spaces",
        metavar="arg1,arg2,...",
        dest="checkpatch_args",
    )
    parser.add_argument(
        "-o",
        default="-",
        type=argparse.FileType("w"),
        help="output JUnit XML file",
        metavar="outfile.xml",
        dest="outfile",
    )
    parser.add_argument(
        "--ignore-check",
        action="store_true",
        default=False,
        help="ignore checkpatch.pl check messages",
        dest="ignore_check",
    )
    parser.add_argument(
        "--ignore-warning",
        action="store_true",
        default=False,
        help="ignore checkpatch.pl warning messages",
        dest="ignore_warning",
    )
    args = parser.parse_args()
    checkpatch_to_junit(args)


if __name__ == "__main__":
    main()
