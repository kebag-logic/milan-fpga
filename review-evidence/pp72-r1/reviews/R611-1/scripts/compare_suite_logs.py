#!/usr/bin/env python3
"""Compare per-suite make logs of two runs (base vs head).

Usage: compare_suite_logs.py BASE_LOG_DIR HEAD_LOG_DIR BASE_TREE HEAD_TREE

Each tree path is replaced by a neutral token first. A line is "suite output"
unless it matches a build-tool pattern (compiler/Verilator/make command lines,
Verilator's own walltime report, unittest's duration line). Prints, per suite,
whether the logs are byte-identical after path normalisation, and every
differing line, labelled TOOL or SUITE. Exit 1 if any SUITE line differs.
"""
import difflib
import re
import sys
from pathlib import Path

base_dir, head_dir, base_tree, head_tree = map(Path, sys.argv[1:5])
TOOL = re.compile(
    r"^(make(\[\d+\])?:|g\+\+|c\+\+|ccache|clang|/usr/bin/|ar |rm |mkdir |cd |echo |python3 -B|"
    r"perl |verilator |.*/verilator(_bin)? |- V e r i l a t i o n|- Verilator:|"
    r"Ran \d+ tests in [\d.]+s$|.*\s-c -o \S+\.o\b|.*-o V\S+\s|.*\.(cpp|o|a|mk)( \\)?$|"
    r"\s+-[A-Za-z]|\s+\S+\.(cpp|o|a|sv)\b)")


def norm(text: str, tree: Path) -> list[str]:
    return text.replace(str(tree), "<TREE>").splitlines()


suite_diffs = 0
for b in sorted(base_dir.glob("*.log")):
    h = head_dir / b.name
    if not h.exists():
        print(f"{b.stem}: MISSING at head")
        suite_diffs += 1
        continue
    bl = norm(b.read_text(errors="replace"), base_tree)
    hl = norm(h.read_text(errors="replace"), head_tree)
    if bl == hl:
        print(f"{b.stem}: identical after path normalisation ({len(bl)} lines)")
        continue
    tool = suite = 0
    lines = []
    for d in difflib.unified_diff(bl, hl, lineterm="", n=0):
        if d.startswith(("---", "+++", "@@")):
            continue
        body = d[1:]
        kind = "TOOL" if TOOL.match(body) else "SUITE"
        if kind == "TOOL":
            tool += 1
        else:
            suite += 1
        lines.append(f"    {kind} {d[:200]}")
    print(f"{b.stem}: {tool} tool lines and {suite} suite lines differ")
    for l in lines:
        if " SUITE " in l[:12] or suite:
            print(l)
    suite_diffs += suite
for h in sorted(head_dir.glob("*.log")):
    if not (base_dir / h.name).exists():
        print(f"{h.stem}: MISSING at base")
        suite_diffs += 1
print(f"suite-output lines differing: {suite_diffs}")
sys.exit(1 if suite_diffs else 0)
