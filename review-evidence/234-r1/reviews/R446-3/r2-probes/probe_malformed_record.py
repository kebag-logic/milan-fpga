#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: malformed fields INSIDE a baseline record, through the gate's command line.

Uses the gate self-test's own fixture (route and standalone measurement
directories and their recorded entries), writes a baseline whose record has one
field of the wrong type, and runs `check` and `check-baseline` as subprocesses.
The round-2 contract: a malformed baseline entry exits 2 with a named reason,
never through a traceback, and exit 1 is reserved for a material regression.

Usage: probe_malformed_record.py <checkout>; exit 0 when every case holds.
"""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(sys.argv[1]).resolve()
OOC = ROOT / "syn/ooc"
sys.path.insert(0, str(OOC))
import pp_resource_gate_selftest as fx  # noqa: E402


def edit(path: list, value):
    def apply(entry: dict) -> None:
        target = entry
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    return apply


CASES = [
    ("record identity is a list", edit(["record", "identity"], ["tool"])),
    ("record identity is a string", edit(["record", "identity"], "Vivado")),
    ("record scopes is a list", edit(["record", "scopes"], [])),
    ("record gated figure LUT is a string", edit(["record", "figures", "LUT"], "1000")),
    ("record gated figure WNS_ns is null", edit(["record", "figures", "WNS_ns"], None)),
    ("record kind is a list", edit(["record", "kind"], ["route"])),
    ("tolerance LUT is a string", edit(["tolerance", "LUT"], "10")),
    ("floor WNS_ns is NaN (written by json as NaN)", edit(["floor", "WNS_ns"], float("nan"))),
]


def main() -> int:
    bad = 0
    with tempfile.TemporaryDirectory(prefix="r446-malformed-") as tmp:
        tmp = Path(tmp)
        root = tmp / "route"
        root.mkdir()
        entry = fx.recorded(root, "route")
        folder = fx.fresh(root, "route")
        fx.plant(folder, fx.SOURCE[0].replace("{repo}", str(root / "arm/repo")), *fx.SOURCE[1:])
        budget = tmp / "budget.md"
        budget.write_text(fx.BUDGET.replace("| `ooc` | +10 | +10 | - | +0 | +0 | +0 | - | - | - | - |\n", ""))
        for label, change in CASES:
            broken = copy.deepcopy(entry)
            change(broken)
            path = tmp / "baseline.json"
            path.write_text(json.dumps({"endpoints": {"route": broken}}))
            for command in (["check", str(folder), "--endpoint", "route"], ["check-baseline", "--budget", str(budget)]):
                result = subprocess.run([sys.executable, "-B", str(OOC / "pp_resource_gate.py"), *command,
                                         "--baseline", str(path)], capture_output=True, text=True)
                out = (result.stdout + result.stderr).strip().splitlines()
                traceback = any(line.startswith("Traceback") for line in out)
                ok = result.returncode == 2 and not traceback
                bad += not ok
                last = out[-1] if out else ""
                print(f"{'OK ' if ok else 'BAD'} {command[0]:<14} {label:<46} rc={result.returncode}"
                      f"{' TRACEBACK' if traceback else ''} | {last[:150]}")
    print(f"malformed record probe: {bad} case(s) not exit 2 with a named reason")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
