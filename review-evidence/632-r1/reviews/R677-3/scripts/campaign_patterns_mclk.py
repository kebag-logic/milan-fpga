#!/usr/bin/env python3
"""Check milan_dp_mclk's planted-defect edits and selector anchors still match
exactly once at the reviewed head. usage: campaign_patterns_mclk.py <repo>"""
import importlib.util, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); tbv = root / "tb/verilator"
sys.path.insert(0, str(root / "scripts")); sys.path.insert(0, str(tbv / "milan_dp_mclk"))
s = importlib.util.spec_from_file_location("mm", tbv / "milan_dp_mclk/mclk_mutants.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
texts = {k: p.read_text() for k, (p, _) in m.SOURCES.items()}
bad = 0
for k, a in m.SELECTOR_ANCHOR.items():
    if texts[k].count(a) != 1: bad += 1; print("[MISS] anchor", k)
for e in m.EDITS:
    if texts[e.source].count(e.pattern) != 1: bad += 1; print("[MISS]", e.source, e.pattern.strip()[:60])
print(f"mclk: {len(m.EDITS)} edits, {len(m.MUTANTS)} mutants, missing {bad}")
sys.exit(1 if bad else 0)
