#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 4): the external reviewer's round-3 cases, re-planted with this reviewer's own script.

R447-3 F1: a JSON-escaped lone surrogate "\\ud800" as (A) an extra endpoint name, (B) an unknown endpoint
field, (C) an unknown file field, (D) a sub-block scope name; plus a lone surrogate in an identity value.
R447-3 F2: a recorded WNS_ns / WHS_ns written as the 401-digit integer literal 10**400.
R447-3 S1: a repeated key. Each runs through `check` (against B's real route, whose inputs differ, so judge()
is reached) and `check-baseline`, as subprocesses with standard output in strict ASCII. Every case must give
rc 2 in both columns, with no traceback and only printable-ASCII output; the control gives check 1 (B's
+625 LUT) and check-baseline 0.

Usage: probe_r447_3_cases.py <checkout> <B-route-dir> <scratch-dir>
"""

import json
import os
from pathlib import Path
import subprocess
import sys

REPO, ROUTE, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
GATE = REPO / "syn/ooc/pp_resource_gate.py"
TEXT = (REPO / "syn/ooc/pp_resource_baseline.json").read_text()
ENV = dict(os.environ, PYTHONIOENCODING="ascii:strict", PYTHONDONTWRITEBYTECODE="1")


def run(*args: object) -> tuple[int, bool, bool, str]:
    result = subprocess.run([sys.executable, "-B", str(GATE), *map(str, args)], capture_output=True, env=ENV,
                            timeout=300)
    out = result.stdout + result.stderr
    lines = out.decode("ascii", "backslashreplace").strip().splitlines()
    return (result.returncode, b"Traceback" in result.stderr, all(b == 10 or 32 <= b <= 126 for b in out),
            (lines[-1] if lines else "")[:140])


def once(old: str, new: str) -> str:
    if TEXT.count(old) < 1:
        raise SystemExit(f"span absent: {old!r}")
    return TEXT.replace(old, new, 1)


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    route = json.loads(TEXT)["endpoints"]["route-1x1"]
    cases = [
        ("control", TEXT, (1, 0)),
        ("A extra endpoint named \\ud800", once('"endpoints": {', '"endpoints": {"\\ud800": '
                                                 + json.dumps(route) + ", "), (2, 2)),
        ("B unknown endpoint field \\ud800", once('"measured":', '"\\ud800": 1, "measured":'), (2, 2)),
        ("C unknown file field \\ud800", once('"endpoints": {', '"\\ud800": 1, "endpoints": {'), (2, 2)),
        ("D scope named \\ud800", once('"u_pp/u_srp": {', '"\\ud800": {"LUT": 1, "FF": 1, "RAMB36": 0, "RAMB18": 0, '
                                       '"DSP": 0, "CARRY4": 0}, "u_pp/u_srp": {'), (2, 2)),
        ("identity tool value holding \\ud800", once('"tool": "', '"tool": "\\ud800'), (2, 0)),
        ("F2 WNS_ns as 10**400 integer literal", once('"WNS_ns": 0.063', '"WNS_ns": 1' + "0" * 400), (2, 2)),
        ("F2 WHS_ns as 10**400 integer literal", once('"WHS_ns": 0.036', '"WHS_ns": 1' + "0" * 400), (2, 2)),
        ("S1 repeated key", once('"measured":', '"measured": "x", "measured":'), (2, 2)),
    ]
    bad = 0
    for label, text, want in cases:
        path = SCRATCH / "baseline.json"
        path.write_text(text)
        got = run("check", ROUTE, "--endpoint", "route-1x1", "--baseline", path)
        audit = run("check-baseline", "--baseline", path)
        ok = (got[0], audit[0]) == want and not got[1] and not audit[1] and got[2] and audit[2]
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {label}: check rc={got[0]} check-baseline rc={audit[0]} want={want} "
              f"traceback={got[1] or audit[1]} ascii={got[2] and audit[2]} | {got[3]} | {audit[3]}")
    print(f"probe_r447_3_cases: {len(cases)} cases, {bad} not as expected")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
