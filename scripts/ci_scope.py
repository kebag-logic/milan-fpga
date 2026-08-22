#!/usr/bin/env python3
"""Classify a changed-file list as docs-only or RTL/tooling relevant.

A submodule pointer is never docs-only. The gitlink entries (`protocol-processor`,
`gptp-processor`, `external`, `third_party/...`) and `.gitmodules` itself move
the RTL the sweep elaborates without touching a file under `hdl/`, so they are
read from `.gitmodules` and classified relevant before any documentation rule
is consulted ([R1] on PR #204). Without `.gitmodules` the rule has nothing to
read and the documentation rules alone decide, which still classifies a bare
gitlink path as relevant because it carries no documentation suffix.
"""

from __future__ import annotations

import argparse
import pathlib
import re
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

GITMODULES = pathlib.Path(__file__).resolve().parent.parent / ".gitmodules"


def submodule_paths(gitmodules: pathlib.Path = GITMODULES) -> tuple[str, ...]:
    """The `path = ...` entries of .gitmodules, derived rather than listed."""
    try:
        text = gitmodules.read_text(encoding="utf-8")
    except OSError:
        return ()
    return tuple(m.group(1).strip()
                 for m in re.finditer(r"^\s*path\s*=\s*(\S+)", text, re.M))


SUBMODULE_PATHS = submodule_paths() + (".gitmodules",)


def is_submodule_path(clean: str) -> bool:
    return (clean in SUBMODULE_PATHS
            or clean.startswith(tuple(p + "/" for p in SUBMODULE_PATHS)))


def is_doc_only_path(path: str) -> bool:
    clean = path.strip()
    while clean.startswith("./"):
        clean = clean[2:]
    if not clean:
        return True
    if is_submodule_path(clean):
        return False
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
    global SUBMODULE_PATHS
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
        # Submodule pointers move RTL without a file under hdl/ ([R1], PR #204).
        (["gptp-processor"], True),
        (["protocol-processor"], True),
        (["external"], True),
        (["third_party/verilog-axis"], True),
        ([".gitmodules"], True),
        (["docs/x.md", "gptp-processor"], True),
    ]
    failures = 0
    for paths, expected in cases:
        got = is_rtl_relevant(paths)
        ok = got == expected
        print(f"  {'ok  ' if ok else 'FAIL'} {paths!r}: rtl={got}")
        failures += 0 if ok else 1

    # The submodule rule is derived from .gitmodules, so prove the derivation
    # saw the tree: every pointer this repository carries must be listed.
    for want in ("protocol-processor", "gptp-processor", "external",
                 "third_party/verilog-axis", ".gitmodules"):
        ok = want in SUBMODULE_PATHS
        print(f"  {'ok  ' if ok else 'FAIL'} submodule rule names {want}")
        failures += 0 if ok else 1

    # Mutation arm: a classifier whose rules file any one pointer as
    # documentation must be caught by the cases above, or they bind nothing.
    # The mutation edits the real rule tables, not a copy of the logic.
    pristine_paths, pristine_files = SUBMODULE_PATHS, set(DOC_FILES)
    try:
        for victim in ("gptp-processor", "protocol-processor", "external",
                       "third_party/verilog-axis", ".gitmodules"):
            SUBMODULE_PATHS = tuple(x for x in pristine_paths if x != victim)
            DOC_FILES.add(victim)
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            DOC_FILES.discard(victim)
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: {victim} filed "
                  "as docs-only is rejected")
            failures += 0 if caught else 1
    finally:
        SUBMODULE_PATHS = pristine_paths
        DOC_FILES.clear()
        DOC_FILES.update(pristine_files)
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
