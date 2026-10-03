#!/usr/bin/env python3
"""Plant route status reports beside the real route measurement and run the gate's CLI.

Usage: probe_route_real.py <repo checkout> <real route measurement directory> <scratch dir>
Mirrors every regular file of the real directory as a symlink (nothing in it is
written), replaces only *_route_status.rpt per case, and runs
`pp_resource_gate.py check <mirror> --endpoint route-1x1` as a subprocess, so a
traceback shows as its real exit status. Prints case, wanted, got, verdict line.
"""
from pathlib import Path
import shutil
import subprocess
import sys

repo, real, scratch = (Path(arg).resolve() for arg in sys.argv[1:4])
REAL = (real / "alinx_ax7101_route_status.rpt").read_text()
LINES = REAL.splitlines(keepends=True)
ROW, ROUTABLE, ROUTED = ([line for line in LINES if label in line][0] for label in
                         ("of nets with routing errors", "of routable nets", "of fully routed nets"))
NETS = ROUTED.split(":")[1].strip()
assert REAL.count(ROW) == REAL.count(ROUTABLE) == REAL.count(ROUTED) == 1
UNROUTED = ROW.replace("     0 :", "    37 :") + "           # of unrouted nets.................... :          37 :\n"
SOME = ROW.replace("     0 :", "     2 :") + "           # of nets with some unrouted pins..... :           2 :\n"
CASES = (
    ("real status, unchanged", {"alinx_ax7101_route_status.rpt": REAL}, 0),
    ("unrouted nets", {"alinx_ax7101_route_status.rpt": REAL.replace(ROW, UNROUTED)}, 1),
    ("nets with some unrouted pins", {"alinx_ax7101_route_status.rpt": REAL.replace(ROW, SOME)}, 1),
    ("routing errors only", {"alinx_ax7101_route_status.rpt": REAL.replace(ROW, ROW.replace("     0 :", "     3 :"))}, 1),
    ("partly routed", {"alinx_ax7101_route_status.rpt": REAL.replace(ROUTED, ROUTED.replace(NETS, str(int(NETS) - 6)))}, 1),
    ("missing report", {}, 2),
    ("duplicated report", {"alinx_ax7101_route_status.rpt": REAL, "alinx_ax7101_post_route_status.rpt": REAL}, 2),
    ("empty report", {"alinx_ax7101_route_status.rpt": ""}, 2),
    ("routable row missing", {"alinx_ax7101_route_status.rpt": REAL.replace(ROUTABLE, "")}, 2),
    ("routed row missing", {"alinx_ax7101_route_status.rpt": REAL.replace(ROUTED, "")}, 2),
    ("both routable rows missing", {"alinx_ax7101_route_status.rpt": REAL.replace(ROUTABLE, "").replace(ROUTED, "")}, 2),
    ("error count unreadable", {"alinx_ax7101_route_status.rpt": REAL.replace(ROW, ROW.replace(" 0 :", " x :"))}, 2),
    ("error count a superscript digit", {"alinx_ax7101_route_status.rpt": REAL.replace(ROW, ROW.replace(" 0 :", " ² :"))}, 2),
    ("report not UTF-8", {"alinx_ax7101_route_status.rpt": b"\xff\xfe" + REAL.encode()}, 2),
    ("report is a directory", {"alinx_ax7101_route_status.rpt/": None}, 2),
)
results = 0
for label, files, wanted in CASES:
    mirror = scratch / "mirror"
    shutil.rmtree(mirror, ignore_errors=True)
    mirror.mkdir(parents=True)
    for path in real.iterdir():
        if path.is_file() and not path.name.endswith("_route_status.rpt"):
            (mirror / path.name).symlink_to(path)
    for name, data in files.items():
        if name.endswith("/"):
            (mirror / name).mkdir()
        elif isinstance(data, bytes):
            (mirror / name).write_bytes(data)
        else:
            (mirror / name).write_text(data)
    run = subprocess.run([sys.executable, "-B", str(repo / "syn/ooc/pp_resource_gate.py"), "check", str(mirror),
                          "--endpoint", "route-1x1"], capture_output=True, text=True, timeout=300)
    text = (run.stdout + run.stderr).strip().splitlines()
    key = [line for line in text if line.startswith(("RESULT", "NOT COMPARABLE", "ROUTE", "route status", "Traceback"))
           or "Error" in line]
    verdict = "OK" if run.returncode == wanted and not any("Traceback" in line for line in text) else "BAD"
    results += verdict == "BAD"
    print(f"{verdict} {label}: wanted {wanted}, got {run.returncode}: {' | '.join(key)}")
shutil.rmtree(scratch / "mirror", ignore_errors=True)
print(f"{len(CASES) - results}/{len(CASES)} as wanted")
