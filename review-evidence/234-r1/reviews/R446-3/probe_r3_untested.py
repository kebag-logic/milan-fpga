#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 3): the head's behaviour on the refusals whose relaxing mutants survive.

For each case the probe_r3_mutants.py survivor names, drive the head gate
through its CLI and record whether the head itself refuses (exit 2, no
traceback). A case the head refuses but no arm exercises is a test gap, not a
code defect.

Usage: probe_r3_untested.py <checkout> <real-route-dir> <scratch-dir>; exit 0 when every case gives 2.
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys

REPO, REAL, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
GATE = REPO / "syn/ooc/pp_resource_gate.py"
SOURCE = json.loads((REPO / "syn/ooc/pp_resource_baseline.json").read_text())


def baseline(name: str, change) -> Path:
    data = json.loads(json.dumps(SOURCE))
    data["endpoints"]["route-1x1"]["record"]["inputs_sha256"] = "0" * 64
    change(data["endpoints"])
    path = SCRATCH / f"{name}.json"
    path.write_text(json.dumps(data, indent=1) + "\n")
    return path


def mirror(name: str, target: str | None = None, edit=None) -> Path:
    folder = SCRATCH / name
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for entry in REAL.iterdir():
        (folder / entry.name).symlink_to(entry)
    if target:
        text = (REAL / target).read_text()
        (folder / target).unlink()
        (folder / target).write_text(edit(text))
    return folder


def hierarchy_cell(column: int, digit: str):
    """Replace one count cell of the first instance row with another script's digit."""
    def edit(text: str) -> str:
        lines = text.splitlines(keepends=True)
        for index, line in enumerate(lines):
            cells = line.split("|")
            if len(cells) == 12 and cells[3].strip().isdigit():
                width = len(cells[column])
                cells[column] = digit.rjust(width - 1) + " "
                lines[index] = "|".join(cells)
                return "".join(lines)
        raise AssertionError("no instance row")
    return "baseline_hierarchy.rpt", edit


def errors_row_twice(text: str) -> str:
    row = next(line for line in text.splitlines(keepends=True) if "nets with routing errors" in line)
    return text.replace(row, row + row, 1)


ROUTE = lambda ends: ends["route-1x1"]["record"]  # noqa: E731
CASES = [
    ("control", None, None, 0),
    ("identity holds an extra key", lambda e: ROUTE(e)["identity"].update({"extra": "x"}), None, 2),
    ("figures hold an extra figure", lambda e: ROUTE(e)["figures"].update({"EXTRA": 1}), None, 2),
    ("a scope holds an extra count", lambda e: ROUTE(e)["scopes"]["wrapper"].update({"EXTRA": 1}), None, 2),
    ("input digest is a number", lambda e: ROUTE(e).update({"inputs_sha256": 123}), None, 2),
    ("input digest is null", lambda e: ROUTE(e).update({"inputs_sha256": None}), None, 2),
    ("the last endpoint (ooc-8x8) has kind 'x'", lambda e: e["ooc-8x8"]["record"].update({"kind": "x"}), None, 2),
    ("routing-errors row twice", None, ("alinx_ax7101_route_status.rpt", errors_row_twice), 2),
    ("hierarchy FF cell in Arabic-Indic digit", None, hierarchy_cell(7, "٣"), 2),
    ("hierarchy DSP cell in Arabic-Indic digit", None, hierarchy_cell(10, "٣"), 2),
]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    bad = 0
    for index, (name, change, edit, want) in enumerate(CASES):
        path = baseline(f"u{index}", change or (lambda e: None))
        folder = mirror(f"u{index}", *(edit or (None, None)))
        result = subprocess.run([sys.executable, "-B", str(GATE), "check", str(folder), "--endpoint", "route-1x1",
                                 "--baseline", str(path)], capture_output=True, text=True, timeout=300)
        lines = (result.stdout + result.stderr).strip().splitlines()
        trace = "Traceback" in result.stderr
        ok = result.returncode == want and not trace
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} check {name:<44} want={want} rc={result.returncode}"
              f"{' TRACEBACK' if trace else ''} | {(lines[-1] if lines else '')[-140:]}")
    print(f"untested-refusal probe: {bad} case(s) where the head does not refuse")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
