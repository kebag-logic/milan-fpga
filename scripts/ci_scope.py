#!/usr/bin/env python3
"""Classify a changed-file list as docs-only or RTL/tooling relevant.

A submodule pointer is never docs-only. The gitlink entries (`protocol-processor`,
`gptp-processor`, `external`, `third_party/...`) and `.gitmodules` itself move
the RTL the sweep elaborates without touching a file under `hdl/`, so they are
read from `.gitmodules` and classified relevant before any documentation rule
is consulted ([R1] on PR #204). Without `.gitmodules` the rule has nothing to
read and the documentation rules alone decide, which still classifies a bare
gitlink path as relevant because it carries no documentation suffix.

Documentation is a path no gate that the docs-only path skips can read
(#444, [R197] F2): a top-level `*.md`, anything under `LICENSES/`, or a
`*.md`, `*.drawio`, `*.svg` or `*.png` under `docs/` other than the pages in
GATE_READ_DOCS. Everything else is relevant whatever its suffix: every file
under `tb/`, `hdl/`, `sw/`, `syn/`, `scripts/`, `tests/` and `configs/` (the
campaign records under `hdl/**/doc/` are read by the tsn_fuzz suite), and
every generator, manifest and budget under `docs/`. A page some skipped gate
also reads stays documentation only where an always-run docs.yml job runs
the same check on it; the policy page names each reader.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from collections.abc import Iterable, Sequence

#: LISTS, not tuples, for the same reason as SUBMODULE_PATHS below: the
#: selftest's mutation arm edits the real rule table in place.
#: Everything below one of these prefixes is documentation.
DOC_PREFIXES = ["LICENSES/"]
#: Under `docs/`, prose and the diagram assets are documentation; a
#: generator, a manifest or a budget beside them is not.
DOCS_TREE = "docs/"
DOCS_TREE_SUFFIXES = [".md", ".drawio", ".svg", ".png"]
#: At the top level, prose only.
TOP_LEVEL_SUFFIXES = [".md"]
#: Pages under `docs/` that Python in GATED_PY_ROOTS names, so a gate the
#: docs-only path skips may read them. Not a list written from memory: the
#: selftest derives the same set from the tree and refuses any difference.
#: The behave suite (rtl-fast's `bdd-conformance`, which docs.yml never runs)
#: asserts on the first two; the third is the page the trace catalogue
#: generator's `--check` compares.
GATE_READ_DOCS = [
    "docs/reference/REGISTER_MAP.md",
    "docs/reference/TRACE_EVENTS.md",
    "docs/testing/MILAN_V12_AUDIT_2026-08-16.md",
]
#: Where the classifier-gated jobs run Python that no docs.yml job runs. The
#: selftest scans it for a documentation path named as a whole string
#: literal or as a `"docs" / ...` join. test_builder.py is left out because
#: docs.yml's `docs-check` runs it on every pull request, every arm that
#: reads a page included; `--require-elaboration` in `elaborate` changes only
#: how a skipped LiteX arm is graded.
GATED_PY_ROOTS = ("tests", "tb", "syn", "sw", "hdl", "avdecc")
DOCS_JOB_PY = ("sw/builder/test_builder.py",)

ROOT = pathlib.Path(__file__).resolve().parent.parent
GITMODULES = ROOT / ".gitmodules"


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
    """Whether one changed path carries documentation and nothing a skipped
    gate reads.

    A submodule pointer is excluded first: it names no suffix of its own, so
    the documentation rules alone would let a moved gitlink pass as prose.
    """
    clean = path.strip()
    while clean.startswith("./"):
        clean = clean[2:]
    if not clean:
        return True
    if is_submodule_path(clean) or clean in GATE_READ_DOCS:
        return False
    if clean.startswith(tuple(DOC_PREFIXES)):
        return True
    if clean.startswith(DOCS_TREE):
        return clean.endswith(tuple(DOCS_TREE_SUFFIXES))
    return "/" not in clean and clean.endswith(tuple(TOP_LEVEL_SUFFIXES))


_LITERAL = re.compile(r"""(["'])([^"'\n]*)\1""")
_DOCS_JOIN = re.compile(r"""(["'])docs\1((?:\s*/\s*(["'])[^"'\n]+\3)+)""")
_SEGMENT = re.compile(r"""["']([^"'\n]+)["']""")


def gated_py_files(root: pathlib.Path = ROOT) -> list[str]:
    """The Python files under GATED_PY_ROOTS, tracked ones when git can say,
    else whatever the tree holds (the no-git docs job runs this too)."""
    run = subprocess.run(["git", "-C", str(root), "ls-files", "--",
                          *GATED_PY_ROOTS], capture_output=True, text=True,
                         check=False)
    if run.returncode == 0 and run.stdout.strip():
        found = run.stdout.split()
    else:
        found = [p.relative_to(root).as_posix() for r in GATED_PY_ROOTS
                 for p in (root / r).rglob("*.py")]
    return sorted(p for p in found
                  if p.endswith(".py") and p not in DOCS_JOB_PY)


def docs_named_by_gated_code(root: pathlib.Path = ROOT) -> dict[str, str]:
    """Each `docs/` page or top-level page a gated module names, mapped to
    the first `file:line` that names it. Comment lines are skipped; a page
    cited inside a longer message is not a whole literal and is not named."""
    named: dict[str, str] = {}
    for rel in gated_py_files(root):
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            found = [m.group(2).strip() for m in _LITERAL.finditer(line)]
            found += ["docs/" + "/".join(_SEGMENT.findall(m.group(2)))
                      for m in _DOCS_JOIN.finditer(line)]
            for page in found:
                top = "/" not in page and (root / page).is_file()
                if (page.startswith(DOCS_TREE) or top) and (
                        page in GATE_READ_DOCS or is_doc_only_path(page)):
                    named.setdefault(page, f"{rel}:{n}")
    return named


def is_rtl_relevant(paths: Iterable[str]) -> bool:
    """Whether a changed-file list can move the RTL, so the heavy jobs must run."""
    changed = [path.strip() for path in paths if path.strip()]
    # An empty diff is treated conservatively. A broken base selection must not
    # turn a real change into a docs-only green.
    return not changed or any(not is_doc_only_path(path) for path in changed)


Case = tuple[list[str], bool]


def _cases() -> list[Case]:
    """The classification table: changed paths and whether they are RTL
    relevant."""
    return [
        (["docs/testing/CI_WORKFLOWS.md"], False),
        (["README.md", "AGENTS.md"], False),
        (["LICENSES/CERN-OHL-W-2.0.txt"], False),
        (["docs/diagrams/x.drawio", "docs/diagrams/x.svg",
          "docs/diagrams/x.png"], False),
        # #444 ([R197] F2): nothing a skipped gate reads is documentation.
        # The campaign records check_results_fresh.py compares in tsn_fuzz.
        (["hdl/ieee1722/avtp/doc/TEST_RESULTS.md"], True),
        (["hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md"], True),
        # The pages the behave suite and the trace generator read.
        (["docs/reference/REGISTER_MAP.md"], True),
        (["docs/testing/MILAN_V12_AUDIT_2026-08-16.md"], True),
        (["docs/reference/TRACE_EVENTS.md"], True),
        # Under docs/, a generator, a manifest, a budget or other non-prose.
        (["docs/traceability/gen_module_matrix.py"], True),
        (["docs/diagrams/PNG_MANIFEST.json"], True),
        (["docs/traceability/untested.budget"], True),
        (["docs/notes.txt"], True),
        # Outside docs/, a test bench README and the diagram assets.
        (["tb/verilator/milan_dp/README.md"], True),
        (["hdl/ieee1722/aaf/doc/x.svg"], True),
        (["cdc_census.drawio"], True),
        (["cdc_census.svg"], True),
        (["docs/x.md", "hdl/ieee1722/avtp/doc/TEST_RESULTS.md"], True),
        # #444: outside the documentation classes nothing is documentation.
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


def _gate_read_arms() -> int:
    """#444 ([R197] F2): the gate-read table is derived, not remembered. The
    pages the gated Python names must be exactly the pages the table files
    as relevant. Returns the failure count."""
    failures = 0
    named = docs_named_by_gated_code()
    for page in sorted(set(named) | set(GATE_READ_DOCS)):
        where = named.get(page, "no gated module")
        ok = page in named and page in GATE_READ_DOCS
        print(f"  {'ok  ' if ok else 'FAIL'} gate-read page {page} "
              f"(named at {where}) is relevant")
        failures += 0 if ok else 1
    return failures


def _mutation_arms(cases: list[Case]) -> int:
    """A classifier whose rules file any one pointer, or any gate-read file,
    as documentation must be caught by the cases, or they bind nothing. The
    mutation edits the real rule tables, not a copy of the logic. Returns
    the failure count."""
    failures = 0
    pristine_paths, pristine_prefixes = list(SUBMODULE_PATHS), list(DOC_PREFIXES)
    pristine_tree = list(DOCS_TREE_SUFFIXES)
    pristine_top = list(TOP_LEVEL_SUFFIXES)
    pristine_read = list(GATE_READ_DOCS)
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
        # #444: each widening of the documentation classes, among them each
        # gate-read file filed back as documentation ([R197] F2), is caught
        # by a case.
        for table, widened in (
                (DOC_PREFIXES, ".github/ISSUE_TEMPLATE/"),
                (DOC_PREFIXES, "LICENSE"),
                (TOP_LEVEL_SUFFIXES, ".rst"),
                (DOC_PREFIXES, "docs/"),
                (DOC_PREFIXES, "hdl/ieee1722/avtp/doc/"),
                (DOC_PREFIXES, "hdl/ieee8021as/gptp_plane/doc/"),
                (DOC_PREFIXES, "tb/"),
                (DOCS_TREE_SUFFIXES, ".py"),
                (DOCS_TREE_SUFFIXES, ".json"),
                (TOP_LEVEL_SUFFIXES, ".svg")):
            table.append(widened)
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            table.remove(widened)
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: {widened} filed "
                  "as docs-only is rejected")
            failures += 0 if caught else 1
        for page in pristine_read:
            GATE_READ_DOCS.remove(page)
            caught = any(is_rtl_relevant(paths) != expected
                         for paths, expected in cases)
            derived = docs_named_by_gated_code()
            GATE_READ_DOCS[:] = pristine_read
            print(f"  {'ok  ' if caught else 'FAIL'} mutation: gate-read "
                  f"{page} filed as docs-only is rejected")
            failures += 0 if caught else 1
            ok = page in derived
            print(f"  {'ok  ' if ok else 'FAIL'} mutation: the scan still "
                  f"names {page} once the table drops it")
            failures += 0 if ok else 1
    finally:
        SUBMODULE_PATHS[:] = pristine_paths
        DOC_PREFIXES[:] = pristine_prefixes
        DOCS_TREE_SUFFIXES[:] = pristine_tree
        TOP_LEVEL_SUFFIXES[:] = pristine_top
        GATE_READ_DOCS[:] = pristine_read
    return failures


def selftest() -> int:
    """Prove the classification table, the derived gate-read table, and that
    dropping any one submodule pointer or gate-read file from the rules is
    caught by a case; 0 when every arm holds."""
    cases = _cases()
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

    failures += _gate_read_arms() + _mutation_arms(cases)
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
