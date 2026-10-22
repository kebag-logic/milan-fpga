#!/usr/bin/env python3
"""For the tdm8render and gmstep campaigns, report each named check that no
harness source line carries as a literal prefix (a static hint only: names
built at run time are listed for a manual look). usage: campaign_names.py <repo>"""
import importlib.util, re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); tbv = root / "tb/verilator"
sys.path.insert(0, str(root / "scripts"))
def load(rel, name):
    s = importlib.util.spec_from_file_location(name, tbv / rel); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def text(*rels): return "\n".join((tbv / r).read_text() for r in rels)
def stem(n):  # the literal head of a check name, before any printf field
    return re.split(r"%|\(|\{", n)[0].strip()[:40]
m = load("milan_dp_render/tdm8_render_mutants.py", "t")
src = text("milan_dp_render/sim_tdm8_render.cpp")
for name, _s, _e, leg, mode, brk in m.MUTATIONS:
    for n in (brk if isinstance(brk, tuple) else (brk,)):
        if stem(n) not in src: print(f"[tdm8render] {name!r}: no literal '{stem(n)}'")
g = load("milan_dp_gm_steps/gmstep_mutants.py", "g")
src = text("milan_dp/sim_gmstep.cpp", "milan_dp/sim_main.cpp") if (tbv/"milan_dp/sim_gmstep.cpp").exists() else ""
for c in g.CONTROLS:
    if stem(c.breaks) not in src: print(f"[gmstep] {c.name!r} ({c.leg}): no literal '{stem(c.breaks)}'")
print("done")
