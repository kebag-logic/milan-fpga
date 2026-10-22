#!/usr/bin/env python3
"""Check that every planted-defect pattern of the datapath render campaigns
matches its source exactly once at the reviewed head (each driver's own
precondition), without building or running anything.
usage: campaign_patterns.py <repo root>"""
import importlib.util, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
tbv = root / "tb/verilator"
sys.path.insert(0, str(root / "scripts"))

def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, tbv / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

bad = total = 0
def chk(campaign, mname, path, pat):
    global bad, total
    total += 1
    n = Path(path).read_text().count(pat)
    if n != 1:
        bad += 1
        print(f"[MISS] {campaign}: {mname!r}: pattern appears {n} time(s) in {Path(path).name}")

m = load("milan_dp_render/tdm8_render_mutants.py", "tdm8m")
for name, src, edits, *_ in m.MUTATIONS:
    for pat, _r in edits:
        chk("tdm8render", name, m.SOURCES[src][0], pat)
print(f"tdm8render: {len(m.MUTATIONS)} mutants")

g = load("milan_dp_gm_steps/gmstep_mutants.py", "gms")
for c in g.CONTROLS:
    chk("gmstep", c.name, g.SOURCES[c.source], c.anchor)
print(f"gmstep: {len(g.CONTROLS)} controls")

f = load("follow_ring/mutants.py", "frm")
for name, _d, dp, cap, *_ in f.MUTANTS:
    for pat, _r in dp:
        chk("follow_ring", name, f.DATAPATH, pat)
    for pat, _r in cap:
        chk("follow_ring", name, f.CAPTURE, pat)
print(f"follow_ring: {len(f.MUTANTS)} mutants")

r = load("milan_dp/render_mutants.py", "rdm")
tab = [v for k, v in vars(r).items() if k.isupper() and isinstance(v, (list, tuple)) and v and isinstance(v[0], tuple) and len(v[0]) >= 3]
print("render_mutants tables:", [k for k, v in vars(r).items() if k.isupper() and isinstance(v, (list, tuple))])
print(f"patterns checked: {total}, missing: {bad}")
sys.exit(1 if bad else 0)
