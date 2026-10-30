#!/usr/bin/env python3
"""Round-2 planted probes (F2, F3) on a disposable copy of a real recorded route set (dcp and .Xil excluded).

usage: round2_probes.py <repo-at-head> <set-root> <scratch> <out-tsv>
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

def keep(text):
    keys = ("selected", "REGRESSION", "WARNING", "NOT COMPARABLE", "RESULT", "not of one run")
    return " | ".join(l.strip() for l in text.splitlines() if any(k in l for k in keys))[:1200]

def has(label, plants, want, need=(), forbid=(), **kw):
    """A probe whose output must also contain every `need` and none of `forbid`."""
    root = fresh("p")
    for fn in plants: fn(root)
    rc, text = run(root, **kw)
    good = rc == want and all(n in text for n in need) and not any(f in text for f in forbid)
    results.append((label, want, rc, "OK" if good else "UNEXPECTED", keep(text)))
    (out.parent / "logs").mkdir(exist_ok=True)
    (out.parent / "logs" / (label.split(":")[0] + ".log")).write_text(text.replace(str(scratch), "<scratch>"))
    print(label, rc, want, "OK" if good else "UNEXPECTED", flush=True)

has("control: copied dev set", [], 0, ("directive ExtraPostPlacementOpt selected", "RESULT: PASS"), ("WARNING",))
# F2: a floor miss with a fall beyond the 0.25 ns timing fall reports both, and still exits 1.
has("F2-wns: every route below the setup floor, the selected one fell 0.42",
    [corner(S, "Slow_0C", 0, "0.020"), summ(S, 0, "0.020"),
     corner(A, "Slow_0C", 0, "0.015"), corner(A, "Slow_85C", 0, "0.015"), summ(A, 0, "0.015"),
     corner(E, "Slow_0C", 0, "0.010"), corner(E, "Slow_85C", 0, "0.010"), summ(E, 0, "0.010")], 1,
    ("directive ExtraPostPlacementOpt selected", "REGRESSION: below the floor 0.03 at Slow_0C; WARNING: fell by more than 0.25 from the record",
     "WARNING: WNS_ns fell from the record by more than the timing fall", "RESULT: MATERIAL REGRESSION"))
has("F2-whs: selected route WHS -0.300 at Fast_85C, a fall of 0.336",
    [corner(S, "Fast_85C", 4, "-0.300"), summ(S, 4, "-0.300")], 1,
    ("directive ExtraPostPlacementOpt selected", "REGRESSION: below the floor 0.0 at Fast_85C; WARNING: fell by more than 0.25 from the record",
     "WARNING: WHS_ns fell from the record by more than the timing fall", "RESULT: MATERIAL REGRESSION"))
has("F2-whs-within: selected route WHS -0.005 at Fast_85C, a fall of 0.041: no warning",
    [corner(S, "Fast_85C", 4, "-0.005"), summ(S, 4, "-0.005")], 1,
    ("REGRESSION: below the floor 0.0 at Fast_85C", "RESULT: MATERIAL REGRESSION"), ("WARNING",))
# F3: a timing summary that disagrees with its route's signoff corners, in either direction, is refused.
has("F3-a: every route's summary WNS 0.010, corners unchanged",
    [summ(S, 0, "0.010"), summ(A, 0, "0.010"), summ(E, 0, "0.010")], 2, ("timing summary's 0.01: the reports are not of one run",))
has("F3-b: the selected route's summary WNS 0.010, corners unchanged",
    [summ(S, 0, "0.010")], 2, ("timing summary's 0.01: the reports are not of one run",))
has("F3-c: the selected route's summary WHS -0.050, corners unchanged",
    [summ(S, 4, "-0.050")], 2, ("worst WHS_ns is 0.028 and the timing summary's -0.05: the reports are not of one run",))
has("F3-d: a selected corner's WNS 0.250 below the summary's 0.303",
    [corner(S, "Slow_85C", 0, "0.250")], 2, ("worst WNS_ns is 0.25 and the timing summary's 0.303",))
has("F3-e: a selected corner's WHS 0.010 below the summary's 0.028",
    [corner(S, "Fast_85C", 4, "0.010")], 2, ("worst WHS_ns is 0.01 and the timing summary's 0.028",))
has("F3-f: a comparison's summary WNS 0.010 below its corners",
    [summ(E, 0, "0.010")], 2, ("timing summary's 0.01: the reports are not of one run",))
out.write_text("label\twant\trc\tverdict\toutput\n" + "".join("\t".join(map(str, r)) + "\n" for r in results))
