#!/usr/bin/env python3
"""Audit the round-2 author directive receipts against the committed resource gate.

Usage: python3 -I directive_probe.py <source-tree> <evidence-root>
  <source-tree>   checkout at the reviewed head (supplies syn/ooc/pp_resource_gate.py
                  and syn/ooc/pp_resource_baseline.json)
  <evidence-root> extracted review-evidence/806-r1 directory (holds MANIFEST.json)

Checks: every manifest entry's published hash and that every file is listed;
the gate's utilization parser on each directive's placed-utilization report;
per-corner WNS/WHS from the author's per-corner table against the build floor
(WNS >= +0.03 ns, WHS >= 0) and against the record with the gate's own
verdict_for; and that each directive script differs from its sibling only on
the place_design line.
"""
import hashlib
import sys as _sys
_sys.dont_write_bytecode = True
import importlib.util
import json
import re
import sys
from pathlib import Path

src, ev = Path(sys.argv[1]), Path(sys.argv[2])
fail = 0

def say(ok, text):
    global fail
    fail += 0 if ok else 1
    print(("PASS " if ok else "FAIL ") + text)

manifest = json.loads((ev / "MANIFEST.json").read_text())
listed = {e["file"] for e in manifest}
on_disk = {str(p.relative_to(ev)) for p in ev.rglob("*") if p.is_file()} - {"MANIFEST.json"}
bad = [e["file"] for e in manifest
       if hashlib.sha256((ev / e["file"]).read_bytes()).hexdigest() != e["published_sha256"]]
say(not bad, f"manifest: {len(manifest)} entries, published hash mismatches {bad}")
say(listed == on_disk, f"manifest coverage: unlisted {sorted(on_disk - listed)}, missing {sorted(listed - on_disk)}")

sys.path.insert(0, str(src / "syn/ooc"))
spec = importlib.util.spec_from_file_location("gate", src / "syn/ooc/pp_resource_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
record = json.loads((src / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]["route-1x1"]
print("record route-1x1 figures:", {k: record["record"]["figures"][k] for k in record["record"]["figures"]})
print("record floor:", record["floor"], "tolerance:", record["tolerance"])

d = ev / "author-r2/receipts/directives"
table = (d / "directive-figures.txt").read_text()
for name in ("AltSpreadLogic_high", "ExtraTimingOpt"):
    print(f"== {name}")
    util = gate.utilization((d / name / "alinx_ax7101_utilization_place.rpt").read_text(), record["record"]["kind"])
    print("gate utilization parse:", util)
    section = table.split(f"## {name}\n", 1)[1].split("\n## ", 1)[0]
    stated = dict(re.findall(r"(\w+) ([0-9.]+)", section.splitlines()[0].split(":", 1)[1]))
    for k in ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "DSP", "BRAM_TILE"):
        if k in util:
            say(float(stated[k]) == float(util[k]), f"{k}: author {stated[k]} == parsed {util[k]}")
    corners = {c: (float(w), float(h)) for c, w, h in
               re.findall(r"^(\w+_\d+C): WNS \+?([0-9.-]+) TNS [0-9.]+ WHS \+?([0-9.-]+)", section, re.M)}
    say(len(corners) == 4, f"four corners listed: {sorted(corners)}")
    wns = min(w for w, _ in corners.values()); whs = min(h for _, h in corners.values())
    say(float(stated["WNS_ns"]) == wns and float(stated["WHS_ns"]) == whs,
        f"stated worst WNS {stated['WNS_ns']} / WHS {stated['WHS_ns']} equal the per-corner minima {wns} / {whs}")
    for c, (w, h) in sorted(corners.items()):
        say(w >= 0.03 and h >= 0, f"{c}: WNS {w} >= 0.03 and WHS {h} >= 0 (build floor)")
    for c in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C"):
        neg = (d / name / f"alinx_ax7101_signoff_{c}_negative.rpt").read_text()
        say("No timing paths found." in neg, f"{c} negative-slack report holds no path")
    rs = (d / name / "alinx_ax7101_route_status.rpt").read_text()
    say(re.search(r"routing errors\.+ :\s+0 :", rs) is not None, "route status: 0 nets with routing errors")
    figs = dict(util, WNS_ns=wns, WHS_ns=whs)
    for k, after in figs.items():
        if k in record["record"]["figures"] and k in record["tolerance"]:
            v, ok = gate.verdict_for(record, k, record["record"]["figures"][k], after)
            print(f"  gate verdict_for {k}: {record['record']['figures'][k]} -> {after}: {v}")
    tcl = (d / name / "baseline_implementation.tcl").read_text()
    say(tcl.count("place_design -directive") == 1 and f"place_design -directive {name}\n" in tcl,
        "script places once, with this directive")
    say("alinx_ax7101_synth.dcp" in tcl.splitlines()[1], "script opens the synthesis checkpoint")
a = (d / "AltSpreadLogic_high/baseline_implementation.tcl").read_text().splitlines()
b = (d / "ExtraTimingOpt/baseline_implementation.tcl").read_text().splitlines()
diff = [(x, y) for x, y in zip(a, b) if x != y]
say(len(a) == len(b) and len(diff) == 1 and diff[0][0].startswith("place_design"), f"scripts differ only at {diff}")
before = (d / "synth-dcp.sha256.before").read_text().split()[0]
after = (d / "synth-dcp.sha256.after").read_text().split()[0]
say(before == after, f"synthesis checkpoint hash unchanged across the runs: {before}")
print("RESULT:", "PASS" if not fail else f"{fail} FAIL")
sys.exit(1 if fail else 0)
