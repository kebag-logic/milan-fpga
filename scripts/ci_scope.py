#!/usr/bin/env python3
"""Classify a changed-file list as docs-only or RTL/tooling relevant.

A submodule pointer is never docs-only. The gitlink entries (`protocol-processor`,
`gptp-processor`, `external`, `third_party/...`) and `.gitmodules` itself move
the RTL the sweep elaborates without touching a file under `hdl/`, so they are
read from `.gitmodules` and classified relevant before any documentation rule
is consulted ([R1] on PR #204). Without `.gitmodules` the rule has nothing to
read and the documentation rules alone decide, which still classifies a bare
gitlink path as relevant because it carries no documentation suffix.

Documentation is only what #444 lists: anything under `docs/` or `LICENSES/`,
any `*.md`, and the diagram assets (`*.drawio` masters, `*.svg` and `*.png`
renders), which only the docs job reads. Everything else, an Issue template
and the root `LICENSE` included, is relevant.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from collections.abc import Iterable, Sequence

#: LISTS, not tuples, for the same reason as SUBMODULE_PATHS below: the
#: selftest's mutation arm edits the real rule table in place.
DOC_PREFIXES = ["docs/", "LICENSES/"]
DOC_SUFFIXES = [".md", ".drawio", ".svg", ".png"]

GITMODULES = pathlib.Path(__file__).resolve().parent.parent / ".gitmodules"


def submodule_paths(gitmodules: pathlib.Path = GITMODULES) -> tuple[str, ...]:
    """The `path = ...` entries of .gitmodules, derived rather than listed."""
    try:
        text = gitmodules.read_text(encoding="utf-8")
    except OSError:
        return ()
    return tuple(m.group(1).strip()
                 for m in re.finditer(r"^\s*path\s*=\s*(\S+)", text, re.M))


#: The rule table `is_submodule_path` consults. A LIST, not a tuple, so the
#: selftest's mutation arm can edit the real table in place: rebinding a
#: module global from inside a function needs a `global` statement, and the
#: arm binds nothing at all if it mutates a copy instead.
SUBMODULE_PATHS = list(submodule_paths()) + [".gitmodules"]


def is_submodule_path(clean: str) -> bool:
    """Whether a path is a gitlink or lives under one, checked before any doc rule."""
    return (clean in SUBMODULE_PATHS
            or clean.startswith(tuple(p + "/" for p in SUBMODULE_PATHS)))


def is_doc_only_path(path: str) -> bool:
    """Whether one changed path carries documentation and nothing a build reads.

    A submodule pointer is excluded first: it names no suffix of its own, so
    the documentation rules alone would let a moved gitlink pass as prose.
    """
    clean = path.strip()
    while clean.startswith("./"):
        clean = clean[2:]
    if not clean:
        return True
    if is_submodule_path(clean):
        return False
    if clean.startswith(tuple(DOC_PREFIXES)):
        return True
    return clean.endswith(tuple(DOC_SUFFIXES))


def is_rtl_relevant(paths: Iterable[str]) -> bool:
    """Whether a changed-file list can move the RTL, so the heavy jobs must run."""
    changed = [path.strip() for path in paths if path.strip()]
    # An empty diff is treated conservatively. A broken base selection must not
    # turn a real change into a docs-only green.
    return not changed or any(not is_doc_only_path(path) for path in changed)


def selftest() -> int:
    """Prove the classification table, and that dropping any one submodule
    pointer from the rules is caught by a case; 0 when every arm holds."""
    cases = [
        (["docs/testing/CI_WORKFLOWS.md"], False),
        (["README.md", "AGENTS.md"], False),
        (["tb/verilator/milan_dp/README.md"], False),
        (["docs/notes.txt"], False),
        (["LICENSES/CERN-OHL-W-2.0.txt"], False),
        (["cdc_census.drawio", "cdc_census.svg",
          "hdl/ieee1722/aaf/doc/x.svg", "docs/diagrams/x.png"], False),
        # #444: outside those four classes nothing is documentation.
        ([".github/ISSUE_TEMPLATE/task.yml"], True),
        (["LICENSE"], True),
        (["notes.rst"], True),
        (["docs/x.md", "hdl/ieee1722/aaf/doc/x.svg.in"], True),
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
    pristine_paths, pristine_prefixes = list(SUBMODULE_PATHS), list(DOC_PREFIXES)
    pristine_suffixes = list(DOC_SUFFIXES)
    try:
        for victim in ("gptp-processor", "protocol-processor", "external",
                       "third_party/verilog-axis", ".gitmodules"):
            SUBMODULE_PATHS[:] = [x for x in pristine_paths if x != victim]
            DOC_PREFIXES[:] = pristine_prefixes + [victim]
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            DOC_PREFIXES[:] = pristine_prefixes
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: {victim} filed "
                  "as docs-only is rejected")
            failures += 0 if caught else 1
        # #444: each widening of the documentation classes back past the
        # listed four is caught by a case.
        for table, widened in ((DOC_PREFIXES, ".github/ISSUE_TEMPLATE/"),
                               (DOC_PREFIXES, "LICENSE"),
                               (DOC_SUFFIXES, ".rst")):
            table.append(widened)
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            table.remove(widened)
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: {widened} filed "
                  "as docs-only is rejected")
            failures += 0 if caught else 1
    finally:
        SUBMODULE_PATHS[:] = pristine_paths
        DOC_PREFIXES[:] = pristine_prefixes
        DOC_SUFFIXES[:] = pristine_suffixes
    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return 1 if failures else 0


def main(argv: Sequence[str]) -> int:
    """Classify the paths given on argv or read from stdin, printing true/false."""
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
