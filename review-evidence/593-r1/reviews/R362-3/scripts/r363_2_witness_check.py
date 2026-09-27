#!/usr/bin/env python3
"""Re-check the other reviewer's round-2 witnesses (as published in their F1/S2 text) at this head.
usage: r363_2_witness_check.py <tree-with-tb/tools>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "tb" / "tools"))
import torture_campaign as tp
h = lambda iv, ev, gm, r: tp.check_release_tu_history(iv, ev, gm_changes_s=gm, observation_resolution_s=r, capture_complete=True)
for name, args, want in (
        ("F1 M01 witness: (0,0.2), step 0, GM -0.0005, R 0.001", ([(0, 0.2)], [0], [-0.0005], 0.001), "FAIL"),
        ("F1 M04 witness: touching (0,0.3),(0.3,0.6)", ([(0, 0.3), (0.3, 0.6)], [0, 0.3], [0], 0.001), "NOT RUN"),
        ("S2: R 0.24, clear 10 ms after GM", ([(0, 0.01)], [], [0], 0.24), "NOT RUN"),
        ("S2: R 0.24, clear 9.9 ms after GM", ([(0, 0.0099)], [], [0], 0.24), "NOT RUN")):
    v, d = h(*args)
    print(f"{'OK' if v == want else 'UNEXPECTED'} {name}: expected={want} actual={v} limit={d.get('resolution_limit_s')}")
