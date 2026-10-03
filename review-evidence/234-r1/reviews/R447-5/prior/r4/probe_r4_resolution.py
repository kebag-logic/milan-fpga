#!/usr/bin/env python3
"""Re-plant the other reviewer's round-3 F1 and F2 cases with this reviewer's own script, as real processes.

Usage: probe_r4_resolution.py <repo checkout> <real A route dir> <real B route dir> <scratch dir>
F1 cases: slack and half-count decimals too long to be finite, on a symlink copy of A's route with one report
edited, judged against the committed baseline with route-1x1's input digest zeroed (so judge() would run).
F2 cases: a route status count of 4401 digits on the same copy; the baseline's route WNS_ns or WHS_ns written as a
401-digit JSON integer, through check on B's real route (inputs differ, so judge() would run) and check-baseline.
Expectation for every edited case: exit 2, a NOT COMPARABLE reason, no traceback. Controls keep their status.
Never writes inside the checkout or the measurement directories.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

repo, a_route, b_route, scratch = (Path(arg).resolve() for arg in sys.argv[1:5])
GATE = repo / "syn/ooc/pp_resource_gate.py"
shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
LONG = "1" + "0" * 400
base = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
zero = json.loads(json.dumps(base))
zero["endpoints"]["route-1x1"]["record"]["inputs_sha256"] = "0" * 64
(scratch / "zero.json").write_text(json.dumps(zero, indent=1))
(scratch / "committed.json").write_text(json.dumps(base, indent=1))
bad = 0


def run(label, want, argv):
    global bad
    env = dict(os.environ, PYTHONIOENCODING="ascii:strict")
    result = subprocess.run([sys.executable, "-B", str(GATE), *map(str, argv)], capture_output=True, text=True,
                            env=env, timeout=900)
    tb = "Traceback" in result.stderr
    line = next((l for l in result.stdout.splitlines() if l.startswith(("NOT COMPARABLE", "RESULT", "baseline PASS"))),
                (result.stdout.strip().splitlines() or [""])[-1])
    ok = result.returncode == want and not tb
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {label}: rc {result.returncode} want {want} traceback {tb} :: {line[:200]}")


def farm(name, file, old, new):
    folder = scratch / name
    folder.mkdir()
    for entry in a_route.iterdir():
        if entry.name != file:
            (folder / entry.name).symlink_to(entry)
    text = (a_route / file).read_text()
    assert old in text, (name, old)
    (folder / file).write_text(text.replace(old, new, 1))
    return folder


timing = (a_route / "baseline_timing.rpt").read_text()
rows = [l for l in timing.split("| Design Timing Summary")[1].splitlines() if l.strip()]
heads = next(i for i, l in enumerate(rows) if "WNS(ns)" in l)
values_row = rows[heads + 2]
values = values_row.split()
util = (a_route / "baseline_utilization.rpt").read_text()
tile_row = next(l for l in util.splitlines() if l.startswith("| Block RAM Tile"))
tile = tile_row.split("|")[2].strip()
status = sorted(a_route.glob("*_route_status.rpt"))[0]
srow = next(l for l in status.read_text().splitlines() if "# of routable nets" in l)
count = srow.split(":")[1].strip()

run("control: A route, zeroed digest", 0, ["check", a_route, "--endpoint", "route-1x1", "--baseline", scratch / "zero.json"])
run("F1 WNS 1e400 as a decimal literal", 2, ["check", farm("wns", "baseline_timing.rpt", values_row,
    values_row.replace(values[0], LONG + ".063", 1)), "--endpoint", "route-1x1", "--baseline", scratch / "zero.json"])
whs_row = values_row.split()
run("F1 WHS 1e400 as a decimal literal", 2, ["check", farm("whs", "baseline_timing.rpt", values_row,
    values_row.replace(" " + values[4] + " ", " " + LONG + ".036 ", 1)), "--endpoint", "route-1x1", "--baseline",
    scratch / "zero.json"])
run("F1 negative WNS of the same length", 2, ["check", farm("nwns", "baseline_timing.rpt", values_row,
    values_row.replace(values[0], "-" + LONG + ".063", 1)), "--endpoint", "route-1x1", "--baseline",
    scratch / "zero.json"])
run("F1 Block RAM Tile of 401 digits .5", 2, ["check", farm("tile", "baseline_utilization.rpt", tile_row,
    tile_row.replace(tile, LONG + ".5", 1)), "--endpoint", "route-1x1", "--baseline", scratch / "zero.json"])
run("F2 route status count of 4401 digits", 2, ["check", farm("status", status.name, srow,
    srow.replace(count, "9" * 4401, 1)), "--endpoint", "route-1x1", "--baseline", scratch / "zero.json"])
run("control: B route, committed baseline", 1, ["check", b_route, "--endpoint", "route-1x1", "--baseline",
    scratch / "committed.json"])
for figure in ("WNS_ns", "WHS_ns"):
    text = (scratch / "committed.json").read_text()
    edited = json.loads(text)
    edited["endpoints"]["route-1x1"]["record"]["figures"][figure] = "@@"
    path = scratch / f"int-{figure}.json"
    path.write_text(json.dumps(edited, indent=1).replace('"@@"', LONG))
    run(f"F2 baseline {figure} as a 401-digit JSON integer, check on B", 2,
        ["check", b_route, "--endpoint", "route-1x1", "--baseline", path])
    run(f"F2 baseline {figure} as a 401-digit JSON integer, check-baseline", 2, ["check-baseline", "--baseline", path])
print(f"resolution probe: {bad} off expectation")
