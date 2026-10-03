#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 3): the other reviewer's round-2 F1 cases, re-planted independently at this head.

Each case edits one field of the route-1x1 entry of the shipped baseline (input
digest zeroed so a real A route copy is judged) or one route status count, and
runs `check` and `check-baseline` through the CLI.

Usage: probe_r447_2_cases.py <checkout> <real-route-dir> <scratch-dir>; exit 0 when every case gives 2 with no traceback.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

REPO, REAL, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
GATE = REPO / "syn/ooc/pp_resource_gate.py"
TEXT = (REPO / "syn/ooc/pp_resource_baseline.json").read_text()


def baseline(name: str, field: str, raw: str) -> Path:
    data = json.loads(TEXT)
    data["endpoints"]["route-1x1"]["record"]["inputs_sha256"] = "0" * 64
    if field == "identity":
        data["endpoints"]["route-1x1"]["record"]["identity"] = json.loads(raw)
    out = json.dumps(data, indent=1)
    if field and field != "identity":
        pattern = {"kind": r'("kind": )"route"', "identity": r'("identity": )\{[^}]*\}',
                   "scopes": r'("scopes": )\{', "LUT": r'("LUT": )50128', "WNS_ns": r'("WNS_ns": )0\.063'}[field]
        replacement = (lambda m: m.group(1) + raw + ("{" if field == "scopes" else "")) if field != "scopes" else (
            lambda m: m.group(1) + raw + ', "unused": {')
        out, n = re.subn(pattern, replacement, out, count=1, flags=re.S)
        assert n == 1, field
    path = SCRATCH / f"{name}.json"
    path.write_text(out + "\n")
    return path


def mirror(name: str, count: str | None) -> Path:
    folder = SCRATCH / name
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for entry in REAL.iterdir():
        (folder / entry.name).symlink_to(entry)
    if count:
        status = "alinx_ax7101_route_status.rpt"
        text = (REAL / status).read_text()
        (folder / status).unlink()
        (folder / status).write_text(re.sub(r"(routing errors\.*[ \t]*:[ \t]*)0", lambda m: m.group(1) + count, text))
    return folder


CASES = [("kind []", "kind", "[]", None), ("kind {}", "kind", "{}", None), ("figures.LUT text", "LUT", '"50128"', None),
         ("figures.LUT null", "LUT", "null", None), ("figures.LUT NaN", "LUT", "NaN", None),
         ("identity text", "identity", '"x"', None), ("identity []", "identity", "[]", None),
         ("scopes []", "scopes", "[]", None), ("figures.WNS_ns NaN", "WNS_ns", "NaN", None),
         ("route errors count superscript", "", "", "²")]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    bad = 0
    for index, (name, field, raw, count) in enumerate(CASES):
        path, folder = baseline(f"c{index}", field, raw), mirror(f"c{index}", count)
        for command in ("check", "check-baseline"):
            if command == "check-baseline" and count:
                continue
            args = ["check", str(folder), "--endpoint", "route-1x1"] if command == "check" else ["check-baseline"]
            result = subprocess.run([sys.executable, "-B", str(GATE), *args, "--baseline", str(path)],
                                    capture_output=True, text=True, timeout=300)
            trace = "Traceback" in result.stderr
            ok = result.returncode == 2 and not trace
            bad += not ok
            last = (result.stdout + result.stderr).strip().splitlines()[-1][-110:]
            print(f"{'OK ' if ok else 'BAD'} {command:<15}{name:<32} rc={result.returncode}{' TRACEBACK' if trace else ''} | {last}")
    print(f"R447-2 F1 cases: {bad} not exit 2")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
