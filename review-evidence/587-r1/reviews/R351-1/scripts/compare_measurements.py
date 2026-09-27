#!/usr/bin/env python3
"""Compare reviewer synthesis reports with the committed 50 MHz manifest.

Usage: compare_measurements.py REPO DEFAULT_GATEWARE ATTRIBUTION_GATEWARE
Reads whole-design utilization and WNS from each reviewer run, hashes the
primitive census and scope-timing files, and compares both with the manifest
metrics and the executor's recorded artifact hashes.
"""
import hashlib, json, re, sys
from pathlib import Path
repo, dg, ag = (Path(a) for a in sys.argv[1:4])
man = json.loads((repo / "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json").read_text())
def util(g):
    t = (g / "baseline_utilization.rpt").read_text()
    def cell(label):
        return int(re.search(r"^\|\s*" + re.escape(label) + r"\s*\|\s*(\d+)", t, re.M).group(1))
    lines = (g / "baseline_timing.rpt").read_text().splitlines()
    i = next(k for k, l in enumerate(lines) if "Design Timing Summary" in l)
    wns = next(float(l.split()[0]) for l in lines[i:i + 12] if re.match(r"^\s*-?\d+\.\d+\s", l))
    carry = int(re.search(r"^\|\s*CARRY4\s*\|\s*(\d+)", t, re.M).group(1))
    return {"LUT": cell("Slice LUTs*"), "logic_LUT": cell("LUT as Logic"), "FF": cell("Slice Registers"),
            "RAMB36": cell("RAMB36/FIFO*"), "RAMB18": cell("RAMB18"), "DSP": cell("DSPs"), "CARRY4": carry, "WNS_ns": wns}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ok = True
for variant, g in (("default", dg), ("attribution", ag)):
    mine = util(g)
    ref = man["measurements"][variant]["metrics"]["alinx_ax7101"]
    same = all(mine[k] == ref[k] for k in mine)
    ok &= same
    print(f"{variant}: reviewer {mine}")
    print(f"{variant}: manifest {{{', '.join(f'{k!r}: {ref[k]}' for k in mine)}}} -> {'EQUAL' if same else 'DIFFERENT'}")
    recs = {Path(r["path"]).name: r["sha256"] for r in man["measurements"][variant]["reports"]}
    for name in ("baseline_cells.tsv", "baseline_scope_timing.tsv"):
        eq = sha(g / name) == recs[name]; ok &= eq
        print(f"{variant}: {name} sha256 {'EQUAL' if eq else 'DIFFERENT'} to executor artifact")
sys.exit(0 if ok else 1)
