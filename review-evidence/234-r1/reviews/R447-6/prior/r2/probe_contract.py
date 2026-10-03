#!/usr/bin/env python3
"""Drive the gate's exit-code contract through its real command line with malformed baselines.

Usage: probe_contract.py <repo checkout> <real route measurement directory> <scratch dir>
Each case edits a copy of the head's pp_resource_baseline.json (route-1x1 entry)
and runs `check` against a symlink mirror of the real route directory, then
`check-baseline` on the same file with the head's AREA_BUDGET.md. The mirror is
the real measurement with +1000 LUT planted and one image digest changed, so it
is a material regression the gate must reject with exit 1 against the recorded
baseline. Contract (issue #234 round 2): a malformed or missing baseline entry
exits 2 with a named reason, never a traceback, never 0 or 1.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo, real, scratch = (Path(arg).resolve() for arg in sys.argv[1:4])
GATE = repo / "syn/ooc/pp_resource_gate.py"
BASE = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
shutil.rmtree(scratch, ignore_errors=True)
mirror = scratch / "mirror"
mirror.mkdir(parents=True)
for path in real.iterdir():
    if path.is_file():
        (mirror / path.name).symlink_to(path)
for name, old, new in (("baseline_utilization.rpt", "| Slice LUTs                 | 50128 |", "| Slice LUTs                 | 51128 |"),):
    text = (real / name).read_text()
    assert text.count(old) == 1, (name, old)
    (mirror / name).unlink()
    (mirror / name).write_text(text.replace(old, new))
images = json.loads((real / "baseline_images.json").read_text())
images[0]["sha256"] = "0" * 64
(mirror / "baseline_images.json").unlink()
(mirror / "baseline_images.json").write_text(json.dumps(images))


def edit(path: str, value):
    def apply(entry):
        *keys, last = path.split(".")
        node = entry
        for key in keys:
            node = node[key]
        node[last] = value
    return apply


NAN, INF = float("nan"), float("inf")
CASES = (
    ("control: the recorded baseline", None),
    ("record kind is a list", edit("record.kind", [])),
    ("record kind is an object", edit("record.kind", {})),
    ("record LUT is a string", edit("record.figures.LUT", "50128")),
    ("record LUT is null", edit("record.figures.LUT", None)),
    ("record LUT is NaN", edit("record.figures.LUT", NAN)),
    ("record WNS is NaN", edit("record.figures.WNS_ns", NAN)),
    ("record identity is a string", edit("record.identity", "x")),
    ("record identity is a list", edit("record.identity", [])),
    ("record scopes is a list", edit("record.scopes", [])),
    ("LUT tolerance is Infinity", edit("tolerance.LUT", INF)),
    ("WNS floor is NaN", edit("floor.WNS_ns", NAN)),
    ("BRAM ceiling is NaN", edit("ceiling.BRAM_TILE", NAN)),
    ("record figures is a list", edit("record.figures", [])),
)
bad = 0
for label, change in CASES:
    data = json.loads(json.dumps(BASE))
    if change:
        change(data["endpoints"]["route-1x1"])
    path = scratch / "baseline.json"
    path.write_text(json.dumps(data))
    row = []
    for argv in (["check", str(mirror), "--endpoint", "route-1x1"], ["check-baseline"]):
        run = subprocess.run([sys.executable, "-B", str(GATE), *argv, "--baseline", str(path)],
                             capture_output=True, text=True, timeout=300)
        text = (run.stdout + run.stderr).splitlines()
        crash = any(line.startswith("Traceback") for line in text)
        last = [line for line in text if line.startswith(("RESULT", "NOT COMPARABLE", "baseline PASS"))
                or line.endswith("Error") or "Error:" in line or "in the budget table" in line
                or ": the record" in line or "malformed" in line]
        row.append(f"{argv[0]} rc {run.returncode}{' TRACEBACK' if crash else ''}: {' | '.join(last[-2:])}")
    print(f"{label}\n    " + "\n    ".join(row))
