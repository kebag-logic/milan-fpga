#!/usr/bin/env python3
"""Drive the head's real command line with the inputs whose refusal no shipped arm kills.

Usage: probe_gaps.py <repo checkout> <real route measurement directory> <scratch dir>
The measurement directory is mirrored by symlinks, so a planted file replaces one link and the
original is never written. Each case prints the exit status the head gives and its reason.
"""
import json, shutil, subprocess, sys
from pathlib import Path

repo, real, scratch = (Path(arg).resolve() for arg in sys.argv[1:4])
gate = repo / "syn/ooc/pp_resource_gate.py"
recorded = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())

def mirror(name):
    folder = scratch / name
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for item in real.iterdir():
        (folder / item.name).symlink_to(item)
    return folder

def plant(folder, name, text=None, data=None):
    (folder / name).unlink()
    if data is not None:
        (folder / name).write_bytes(data)
    else:
        (folder / name).write_text(text)

def gate_run(*argv):
    done = subprocess.run([sys.executable, "-B", str(gate), *map(str, argv)], capture_output=True, text=True,
                          errors="backslashreplace")
    trace = " TRACEBACK" if "Traceback" in done.stderr else ""
    last = (done.stderr.strip().splitlines() or done.stdout.strip().splitlines() or [""])[-1]
    return f"rc {done.returncode}{trace}: {last[:170]}"

status = (real / "alinx_ax7101_route_status.rpt").read_text()
error_row = "       # of nets with routing errors.......... :           0 :\n"
assert status.count(error_row) == 1
folder = mirror("dup-error-row")
plant(folder, "alinx_ax7101_route_status.rpt", status.replace(error_row, error_row * 2))
print("1 route status with two 'nets with routing errors' rows (both 0); check:", gate_run("check", folder, "--endpoint", "route-1x1"))

folder = mirror("undecodable-status")
plant(folder, "alinx_ax7101_route_status.rpt", data=status.encode() + b"\xff\xfe")
print("2 route status report that is not UTF-8; check:", gate_run("check", folder, "--endpoint", "route-1x1"))

budget = scratch / "budget-not-utf8.md"
budget.write_bytes((repo / "docs/design/AREA_BUDGET.md").read_bytes() + b"\xff\xfe\n")
print("3 budget page that is not UTF-8; check-baseline:", gate_run("check-baseline", "--budget", budget))

timing = (real / "baseline_timing.rpt").read_text()
row = "      0.063        0.000                      0               179432        0.036        0.000                      0               179351 "
assert timing.count(row) == 1
folder = mirror("ths-zero")
plant(folder, "baseline_timing.rpt", timing.replace(row, row.replace("179351", "     0")))
print("4 timing summary with TNS endpoints 179432 and THS endpoints 0; check:", gate_run("check", folder, "--endpoint", "route-1x1"))

def baseline_case(label, change):
    data = json.loads(json.dumps(recorded))
    change(data["endpoints"]["route-1x1"]["record"]["identity"])
    path = scratch / "baseline.json"
    path.write_text(json.dumps(data, indent=1))
    print(label, "check:", gate_run("check", real, "--endpoint", "route-1x1", "--baseline", path),
          "| check-baseline:", gate_run("check-baseline", "--baseline", path))

baseline_case("5 standalone clock list holding a number;", lambda ident: ident.update({"standalone_clock_ns": [5]}))
baseline_case("6 identity with an extra key;", lambda ident: ident.update({"extra": "x"}))
