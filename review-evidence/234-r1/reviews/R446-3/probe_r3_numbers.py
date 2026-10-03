#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 3): numbers that pass the text guards but are not finite floats.

Builds a symlink mirror of one real route measurement directory (every entry
linked except the file a case edits), writes a copy of the baseline whose
route-1x1 input digest is all zeros (so the candidate is judged, not refused as
"identical inputs"), plants one variant per case and runs
`pp_resource_gate.py check --endpoint route-1x1` and `check-baseline` as
subprocesses.

Usage: probe_r3_numbers.py <checkout> <real-route-dir> <scratch-dir>
Prints one line per case: want, got, traceback or not, last output line.
Exit 0 only when every case meets the published contract: `check` exits 0
within tolerance, 1 for a material regression only, 2 for every input it
cannot judge, never through a traceback; NaN, Infinity or a number too large
to be finite gives 2; a non-finite WNS or WHS is refused with 2.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

REPO, REAL, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
GATE = REPO / "syn/ooc/pp_resource_gate.py"
STATUS = "alinx_ax7101_route_status.rpt"
BIG = "1" + "0" * 400
HUGE_COUNT = "1" + "0" * 4400


def mirror(name: str, edit=None) -> Path:
    folder = SCRATCH / name
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for entry in REAL.iterdir():
        (folder / entry.name).symlink_to(entry)
    if edit:
        target, change = edit
        text = (REAL / target).read_text()
        (folder / target).unlink()
        (folder / target).write_text(change(text))
    return folder


def baseline(name: str, change=None) -> Path:
    text = (REPO / "syn/ooc/pp_resource_baseline.json").read_text()
    data = json.loads(text)
    data["endpoints"]["route-1x1"]["record"]["inputs_sha256"] = "0" * 64
    out = json.dumps(data, indent=1)
    if change:
        out = change(out)
    path = SCRATCH / f"{name}.json"
    path.write_text(out + "\n")
    return path


def run(*args: str) -> tuple[int, bool, str]:
    result = subprocess.run([sys.executable, "-B", str(GATE), *args], capture_output=True, text=True, timeout=300)
    lines = (result.stdout + result.stderr).strip().splitlines()
    last = lines[-1] if lines else ""
    return result.returncode, "Traceback" in result.stderr, last[:150]


def timing_slack(column: int, value: str):
    """Replace the WNS (0) or WHS (4) value on the Design Timing Summary value row."""
    def change(text: str) -> str:
        head, _, tail = text.partition("| Design Timing Summary")
        lines = tail.splitlines(keepends=True)
        heads = next(i for i, line in enumerate(lines) if "WNS(ns)" in line)
        row = heads + 1
        while not lines[row].strip() or set(lines[row].strip()) <= set("- "):
            row += 1
        token = list(re.finditer(r"\S+", lines[row]))[column]
        lines[row] = lines[row][:token.start()] + value + lines[row][token.end():]
        return head + "| Design Timing Summary" + "".join(lines)
    return "baseline_timing.rpt", change


def status_count(label: str, value: str):
    def change(text: str) -> str:
        pattern = re.compile(r"^([ \t]*#[ \t]*of[ \t]+" + re.escape(label) + r"\.*[ \t]*:[ \t]*)(\S+)", re.M)
        new, n = pattern.subn(lambda m: m.group(1) + value, text)
        assert n == 1, (label, n)
        return new
    return STATUS, change


def figure(name: str, value: str):
    def change(text: str) -> str:
        # the route-1x1 record figures appear first in the file
        new, n = re.subn(r'("' + name + r'": )-?[0-9.]+', lambda m: m.group(1) + value, text, count=1)
        assert n == 1
        return new
    return change


CASES = [
    # name, directory edit, baseline change, want check, want check-baseline
    ("control: real A route, digest differs", None, None, 0, 0),
    ("WNS slack of 401 digits (float() reads inf)", timing_slack(0, BIG + ".063"), None, 2, 0),
    ("WHS slack of 401 digits (float() reads inf)", timing_slack(4, BIG + ".036"), None, 2, 0),
    ("WNS slack of -401 digits (float() reads -inf)", timing_slack(0, "-" + BIG + ".063"), None, 2, 0),
    ("control: WNS slack 0.500 (finite, judged)", timing_slack(0, "0.500"), None, 0, 0),
    ("Block RAM Tile used of 401 digits + .5 (float() reads inf)",
     ("baseline_utilization.rpt", lambda text: text.replace("| Block RAM Tile    | 92.5 |",
                                                             f"| Block RAM Tile    | {BIG}.5 |", 1)), None, 2, 0),
    ("route status count of 4401 digits", status_count("routable nets", HUGE_COUNT), None, 2, 0),
    ("baseline route WNS_ns recorded as a 401-digit JSON integer", None, figure("WNS_ns", BIG), 2, 2),
    ("baseline route WHS_ns recorded as a 401-digit JSON integer", None, figure("WHS_ns", BIG), 2, 2),
    ("control: baseline route WNS_ns recorded as 1e400 (decimal)", None, figure("WNS_ns", "1e400"), 2, 2),
]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    bad = 0
    for index, (name, edit, change, want_check, want_base) in enumerate(CASES):
        folder = mirror(f"case{index}", edit)
        path = baseline(f"case{index}", change)
        for command, want in (("check", want_check), ("check-baseline", want_base)):
            args = ["check", str(folder), "--endpoint", "route-1x1"] if command == "check" else ["check-baseline"]
            rc, trace, last = run(*args, "--baseline", str(path))
            ok = rc == want and not trace
            bad += not ok
            print(f"{'OK ' if ok else 'BAD'} {command:<15}{name:<62} want={want} rc={rc}"
                  f"{' TRACEBACK' if trace else ''} | {last}")
    print(f"{bad} case(s) not as the contract states")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
