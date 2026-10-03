#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: drive the resource gate's route status reader on a real route directory.

Builds a symlink copy of one real route measurement directory (every entry
linked except the route status report), plants one route status variant per
case and runs `pp_resource_gate.py check --endpoint route-1x1` as a subprocess.

Usage: probe_route_status.py <checkout> <real-route-dir> <scratch-dir>
Prints one line per case (want, got, verdict, reason line); exit 0 only when
every case meets the reviewer's expectation. Cases marked CONTRACT carry the
exit status the published contract states (unreadable -> 2, incomplete -> 1).
"""

from pathlib import Path
import shutil
import subprocess
import sys

REPO, REAL, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
NAME = "alinx_ax7101_route_status.rpt"
CLEAN = (REAL / NAME).read_text()
ROUTABLE = "       # of routable nets..................... :      105566 :\n"
ROUTED = "           # of fully routed nets............. :      105566 :\n"
ERRORS = "       # of nets with routing errors.......... :           0 :\n"
assert all(CLEAN.count(line) == 1 for line in (ROUTABLE, ROUTED, ERRORS)), "real report layout changed"


def sub(old: str, new: str) -> str:
    return CLEAN.replace(old, new)


CASES = [
    # (label, want, files: {name: text or None for a directory}, note)
    ("real report, clean", 0, {NAME: CLEAN}),
    ("routing errors with unrouted pins", 1, {NAME: sub(ROUTED, ROUTED.replace("105566", "105529")).replace(
        ERRORS, ERRORS.replace("          0", "         37")
        + "           # of nets with some unrouted pins.. :          37 :\n")}),
    ("routing errors only (overlaps)", 1, {NAME: sub(ERRORS, ERRORS.replace("          0", "          3"))}),
    ("unrouted nets row, partly routed", 1, {NAME: sub(ROUTED, ROUTED.replace("105566", "105529")
                                                      + "           # of unrouted nets................. :"
                                                      "          37 :\n")}),
    ("partly routed, no error row moved", 1, {NAME: sub(ROUTED, ROUTED.replace("105566", "105565"))}),
    ("report missing", 2, {}),
    ("report duplicated", 2, {NAME: CLEAN, "copy_route_status.rpt": CLEAN}),
    ("report empty", 2, {NAME: ""}),
    ("report is a directory", 2, {NAME: None}),
    ("report not UTF-8", 2, {NAME: b"\xff\xfe" + CLEAN.encode()}),
    ("error row repeated", 2, {NAME: sub(ERRORS, ERRORS * 2)}),
    ("error count negative", 2, {NAME: sub(ERRORS, ERRORS.replace("          0", "         -1"))}),
    ("routable row only removed", 2, {NAME: sub(ROUTABLE, "")}),
    ("CONTRACT both routable and fully routed rows removed", 2, {NAME: sub(ROUTABLE, "").replace(ROUTED, "")}),
    ("CONTRACT both rows relabelled", 2, {NAME: sub(ROUTABLE, ROUTABLE.replace("routable nets", "nets to route"))
                                         .replace(ROUTED, ROUTED.replace("fully routed nets", "routed nets...."))}),
    ("CONTRACT wholly unrouted layout (no fully routed row)", 1,
     {NAME: sub(ROUTED, "           # of unrouted nets................. :      105566 :\n")
      .replace(ERRORS, ERRORS.replace("          0", "     105566")
               + "           # of unrouted nets................. :      105566 :\n")}),
]


def main() -> int:
    bad = 0
    for label, want, files in CASES:
        folder = SCRATCH / "route-status-probe"
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        for entry in REAL.iterdir():
            if not entry.name.endswith("_route_status.rpt"):
                (folder / entry.name).symlink_to(entry)
        for name, text in files.items():
            if text is None:
                (folder / name).mkdir()
            elif isinstance(text, bytes):
                (folder / name).write_bytes(text)
            else:
                (folder / name).write_text(text)
        result = subprocess.run([sys.executable, "-B", str(REPO / "syn/ooc/pp_resource_gate.py"), "check",
                                 str(folder), "--endpoint", "route-1x1"], capture_output=True, text=True,
                                timeout=300)
        lines = (result.stdout + result.stderr).splitlines()
        reason = next((line for line in lines if any(key in line for key in (
            "NOT COMPARABLE", "ROUTE INCOMPLETE", "route status:", "Traceback"))), lines[-1] if lines else "")
        verdict = "OK" if result.returncode == want else "BAD"
        bad += verdict == "BAD"
        print(f"{verdict} want {want} got {result.returncode}: {label}: {reason}")
    shutil.rmtree(SCRATCH / "route-status-probe", ignore_errors=True)
    print(f"route status probe: {len(CASES) - bad}/{len(CASES)} as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
