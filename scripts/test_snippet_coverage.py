#!/usr/bin/env python3

"""
Fail if any single pyteen sample snippet has a too low coverage.
"""

import json
import re
import sys
from os.path import basename


def test_snippets_coverage(coverage_path="coverage.json", min_threshold=80):
    js = json.load(open(coverage_path))
    failed = False
    for path, data in js["files"].items():
        if re.match("test.*\.py", basename(path)):
            continue
        cov = data["summary"]["percent_covered"]
        print(f"{path}, {cov} % coverage (min: 80 %)")
        if cov < 80:
            failed = True
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        test_snippets_coverage(path)
    except IndexError:
        test_snippets_coverage()
