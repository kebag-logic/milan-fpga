#!/usr/bin/env python3
"""Classify a changed-file list as docs-only or RTL/tooling relevant."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable, Sequence

DOC_PREFIXES = (
    "docs/",
    "historical_now_obsolete/",
    ".github/ISSUE_TEMPLATE/",
)
DOC_FILES = {
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "REQUIREMENTS.md",
    "SECURITY.md",
}
DOC_SUFFIXES = (".md", ".rst")


def is_doc_only_path(path: str) -> bool:
    clean = path.strip()
    while clean.startswith("./"):
        clean = clean[2:]
    if not clean:
        return True
    if clean in DOC_FILES:
        return True
    if clean.startswith(DOC_PREFIXES):
        return True
    return clean.endswith(DOC_SUFFIXES)


def is_rtl_relevant(paths: Iterable[str]) -> bool:
    changed = [path.strip() for path in paths if path.strip()]
    # An empty diff is treated conservatively. A broken base selection must not
    # turn a real change into a docs-only green.
    return not changed or any(not is_doc_only_path(path) for path in changed)


def selftest() -> int:
    cases = [
        (["docs/testing/CI_WORKFLOWS.md"], False),
        (["README.md", "AGENTS.md"], False),
        ([".github/ISSUE_TEMPLATE/task.yml"], False),
        (["docs/notes.txt"], False),
        (["requirements.txt"], True),
        (["hdl/milan/milan_datapath.sv"], True),
        (["scripts/lint_rtl.py"], True),
        ([".github/workflows/rtl.yml"], True),
        (["docs/x.md", "tb/verilator/cdc/Makefile"], True),
        ([], True),
    ]
    failures = 0
    for paths, expected in cases:
        got = is_rtl_relevant(paths)
        ok = got == expected
        print(f"  {'ok  ' if ok else 'FAIL'} {paths!r}: rtl={got}")
        failures += 0 if ok else 1
    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return 1 if failures else 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv[1:])
    if args.selftest:
        return selftest()
    paths = args.paths or [line.rstrip("\n") for line in sys.stdin]
    print("true" if is_rtl_relevant(paths) else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
