#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: mutants the shipped campaign does not list, run against the shipped self-test.

Each mutant edits one unique span of syn/ooc/pp_resource_gate.py in a temporary
copy (with its two sibling modules) and runs `--selftest`. KILLED means the
self-test exited non-zero; the first AssertionError line is shown as the reason.

Usage: probe_extra_mutants.py <checkout> [--jobs N]; exit 0 always (report only).
"""

import ast
import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(sys.argv[1]).resolve() / "syn/ooc"
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
SOURCE = (HERE / "pp_resource_gate.py").read_text()
MUTANTS = {
    "control": None,
    "check-baseline compares tolerances only": ("        for field in POLICY:\n            held =",
                                                 '        for field in ("tolerance",):\n            held ='),
    "check-baseline compares table figures only": (
        "            for figure in sorted(set(held) | set(table[name][field])):\n",
        "            for figure in sorted(set(table[name][field])):\n"),
    "budget floors read as zero": ("                table[name[1]][field][figure] = float(value[1])\n",
                                   '                table[name[1]][field][figure] = 0.0 if field == "floor" '
                                   "else float(value[1])\n"),
    "budget ceiling column ignored": ('"BRAM tile ceiling": ("ceiling", ("BRAM_TILE",))}',
                                      '"BRAM tile ceiling": ("ceiling", ())}'),
    "Slice row and gate removed together": ('"Slice": "SLICE",\n', "\n"),
    "timed endpoints at zero accepted": ("value.isdigit() and int(value) > 0 for value in paths",
                                         "value.isdigit() and int(value) >= 0 for value in paths"),
    "timed endpoint columns optional": ("    if not paths or not all(", "    if not all("),
    "route status: routable rows may both be absent (as shipped)": None,
    "routing-error label exact": ('    if len(counts.get("nets with routing errors", [])) != 1:\n',
                                  '    if len(counts.get("nets with routing errors", [0])) != 1:\n'),
    "improvement report on timing only": ("        gain = after - before if figure in TIMING else before - after\n",
                                          "        gain = after - before if figure in TIMING else 0\n"),
    "check skips the ceiling list": ('        for figure in CEILINGS[kind]:\n', '        for figure in ():\n'),
}
EXTRA = {"Slice row and gate removed together": ('"route": ("LUT", "FF", "SLICE", ', '"route": ("LUT", "FF", ')}


def run(name: str, change) -> str:
    if change is None and name != "control":
        return f"{'NOTE':<9} {name:<62} | not a mutant: recorded for the route-status finding"
    text = SOURCE
    if change is not None:
        for old, new in [change] + ([EXTRA[name]] if name in EXTRA else []):
            if text.count(old) != 1:
                return f"{'NOT-APPL':<9} {name:<62} | span not unique ({text.count(old)})"
            text = text.replace(old, new)
    ast.parse(text)
    with tempfile.TemporaryDirectory(prefix="r446-extra-mutant-") as tmp:
        for sibling in ("pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
            shutil.copy2(HERE / sibling, Path(tmp) / sibling)
        (Path(tmp) / "pp_resource_gate.py").write_text(text)
        result = subprocess.run([sys.executable, "-B", str(Path(tmp) / "pp_resource_gate.py"), "--selftest"],
                                capture_output=True, text=True, timeout=300)
    out = (result.stdout + result.stderr).splitlines()
    reason = next((line for line in out if "AssertionError" in line or "Error" in line), out[-1] if out else "")
    if name == "control":
        verdict = "CONTROL" if result.returncode == 0 else "CTRL-BAD"
    else:
        verdict = "KILLED" if result.returncode else "SURVIVED"
    return f"{verdict:<9} {name:<62} | {reason[:170]}"


with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
    for line in pool.map(lambda item: run(*item), MUTANTS.items()):
        print(line)
