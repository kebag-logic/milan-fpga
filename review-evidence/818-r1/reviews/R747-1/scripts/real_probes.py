#!/usr/bin/env python3
"""Planted probes on a disposable copy of a real recorded route set (dcp and .Xil excluded).

usage: real_probes.py <repo-at-head> <set-root> <scratch> <out-tsv>
Each probe copies the set, rebinds the comparison scripts to the copy's shipping checkpoint path (as the recipe
would have written them there), applies its plants, runs the head gate's check (or record), and records exit
status and the decisive output lines.
"""
import shutil, subprocess, sys
from pathlib import Path

repo, src, scratch, out = (Path(a).resolve() for a in sys.argv[1:5])
GATE = [sys.executable, "-B", str(repo / "syn/ooc/pp_resource_gate.py")]
DIRS = ("ax7101/gateware", "ax7101-AltSpreadLogic_high", "ax7101-ExtraTimingOpt")
S, A, E = DIRS
CORNER = "alinx_ax7101_signoff_{}_timing.rpt"

def summary_line(text):
    i = text.index("| Design Timing Summary"); lines = text[i:].splitlines()
    h = next(k for k, l in enumerate(lines) if "WNS(ns)" in l)
    return lines[h + 2]

def set_slack(path, col, value):
    """Replace column col (0 WNS, 4 WHS) of the Design Timing Summary row in one report."""
    text = path.read_text(); row = summary_line(text); cells = row.split()
    old = cells[col]; new_row = row.replace(old, value.rjust(len(old)), 1) if col == 0 else None
    if col == 4:
        idx = [i for i in range(len(row)) if row.startswith(old, i)]
        # the fifth whitespace-separated token: locate by token positions
        pos, n = 0, 0
        for tok in row.split():
            pos = row.index(tok, pos)
            if n == 4: break
            pos += len(tok); n += 1
        new_row = row[:pos] + value.rjust(len(old)) + row[pos + len(old):]
    path.write_text(text.replace(row, new_row, 1))

def fresh(name):
    root = scratch / name
    shutil.rmtree(root, ignore_errors=True)
    for d in DIRS:
        shutil.copytree(src / d, root / d, ignore=shutil.ignore_patterns("*.dcp", ".Xil"), symlinks=True)
    for d in (A, E):
        f = root / d / "baseline_implementation.tcl"
        f.write_text(f.read_text().replace(str(src / S), str(root / S)))
    return root

def run(root, *extra, cmd="check", sets=True, baseline=None):
    args = [cmd, str(root / S), "--endpoint", "route-1x1"]
    if sets: args += ["--comparison", str(root / A), "--comparison", str(root / E)]
    args += list(extra)
    if baseline: args += ["--baseline", str(baseline)]
    r = subprocess.run(GATE + args, capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout + r.stderr

def keep(text):
    keys = ("selected", "REGRESSION", "WARNING", "NOT COMPARABLE", "RESULT", "ROUTE INCOMPLETE", "marked")
    return " | ".join(l.strip() for l in text.splitlines() if any(k in l for k in keys))[:900]

results = []
def probe(label, plants, want, *extra, **kw):
    root = fresh("p")
    for fn in plants: fn(root)
    rc, text = run(root, *extra, **kw)
    results.append((label, want, rc, "OK" if rc == want else "UNEXPECTED", keep(text)))
    print(label, rc, want, flush=True)

def corner(d, c, col, v):
    return lambda r: set_slack(r / d / CORNER.format(c), col, v)
def summ(d, col, v):
    return lambda r: set_slack(r / d / "baseline_timing.rpt", col, v)
def edit(d, name, old, new, count=1):
    def f(r):
        p = r / d / name; t = p.read_text()
        assert t.count(old) >= 1, (p, old); p.write_text(t.replace(old, new, count))
    return f

probe("control: copied dev set", [], 0)
probe("selected route misses the hold floor at Fast_85C only (summary WHS follows)",
      [corner(S, "Fast_85C", 4, "-0.005"), summ(S, 4, "-0.005")], 1)
probe("selected route misses the setup floor at Slow_0C only; comparisons too (best below floor)",
      [corner(S, "Slow_0C", 0, "0.020"), summ(S, 0, "0.020"),
       corner(A, "Slow_0C", 0, "0.015"), corner(A, "Slow_85C", 0, "0.015"), summ(A, 0, "0.015"),
       corner(E, "Slow_0C", 0, "0.010"), corner(E, "Slow_85C", 0, "0.010"), summ(E, 0, "0.010")], 1)
probe("shipping below the setup floor, best comparison above: passes naming AltSpreadLogic_high",
      [corner(S, "Slow_0C", 0, "0.020"), corner(S, "Slow_85C", 0, "0.020"), summ(S, 0, "0.020")], 0)
probe("selected corner report disagrees with the summary (another run)", [corner(S, "Slow_85C", 0, "0.250")], 2)
probe("comparison corner report missing", [lambda r: (r / E / CORNER.format("Fast_0C")).unlink()], 2)
probe("comparison script with one extra command", [edit(A, "baseline_implementation.tcl",
      "place_design -directive AltSpreadLogic_high", "place_design -directive AltSpreadLogic_high\nset_param x 1")], 2)
probe("comparison script opening another checkpoint", [edit(E, "baseline_implementation.tcl",
      "ax7101/gateware/alinx_ax7101_synth.dcp", "ax7101/other/alinx_ax7101_synth.dcp")], 2)
probe("comparison of another tool build", [edit(E, "baseline_utilization.rpt", "Build ", "Build 9")], 2)
probe("comparison of another design name in its report", [edit(A, "baseline_utilization.rpt",
      "| Design       : alinx_ax7101", "| Design       : other_top")], 2)
probe("comparison incomplete route, not selected", [edit(E, "alinx_ax7101_route_status.rpt",
      "with routing errors.......... :           0 :", "with routing errors.......... :           2 :")], 1)
probe("selected route LUT over tolerance (+588 against 500)", [edit(S, "baseline_utilization.rpt", "| Slice LUTs                 | 51801 |",
      "| Slice LUTs                 | 52600 |")], 1)
probe("unmarked single route", [], 2, sets=False)
probe("set and mark together", [], 2, "--shipping-selection")
root_holder = []
def self_comparison(label):
    root = fresh("p")
    rc, text = run(root, "--comparison", str(root / S), "--comparison", str(root / A), sets=False)
    results.append((label, 2, rc, "OK" if rc == 2 else "UNEXPECTED", keep(text)))
self_comparison("shipping route also given as a comparison")
def recorded(label):
    root = fresh("p")
    base = scratch / "baseline.json"; shutil.copy2(repo / "syn/ooc/pp_resource_baseline.json", base)
    for fn in [corner(A, "Slow_0C", 0, "0.400"), corner(A, "Slow_85C", 0, "0.400"), summ(A, 0, "0.400")]: fn(root)
    rc, text = run(root, "--write", cmd="record", baseline=base)
    rc2, text2 = run(root, "--baseline", str(base))
    rc3 = subprocess.run(GATE + ["check-baseline", "--baseline", str(base)], capture_output=True, text=True).returncode
    import json
    flow = json.loads(base.read_text())["endpoints"]["route-1x1"]["record"]["identity"]["flow"]
    placed = [l for l in flow if l.startswith("place_design")]
    results.append((label, "0/0/0", f"{rc}/{rc2}/{rc3}", "OK" if (rc, rc2, rc3) == (0, 0, 0) else "UNEXPECTED",
                    keep(text) + " || record flow " + str(placed) + " || recheck " + keep(text2)))
recorded("record --write of a set whose best is AltSpreadLogic_high, then check and check-baseline")
out.write_text("label\twant\trc\tverdict\toutput\n" + "".join("\t".join(map(str, r)) + "\n" for r in results))
