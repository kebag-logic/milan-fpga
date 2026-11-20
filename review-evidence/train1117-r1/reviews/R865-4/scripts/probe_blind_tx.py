#!/usr/bin/env python3
"""Reviewer probe: the re-anchored THE TRANSMIT control (flip_grade.channel_controls) against a detector blinded by
one ms (floor of the row instead of its ceiling) and against the tree's own. Usage: probe_blind_tx.py <repo>"""
import math, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tb/verilator/ctrl_service_budget"))
import rows_tiers, flip_grade
own = flip_grade.channel_controls(repo)
print("own detector: escaped =", own)
real = rows_tiers.tx_statements
def blind(root, points=rows_tiers.POINTS, texts=None):
    out = []
    for point in points:
        i = rows_tiers.point_inputs(root, point, texts)
        w = rows_tiers.solve('tx', i, rows_tiers.BUILT)[0]
        if w is None or i.tx_stated < math.floor(w - 1e-9):
            out.append(f'{point}: CTRL_LOOP_TX_MS states {i.tx_stated} ms, under')
    return out
rows_tiers.tx_statements = blind
b = flip_grade.channel_controls(repo)
print("blinded detector: escaped =", b)
print("PROBE", "PASS" if not own and flip_grade.CHANNEL_CONTROLS[1] in b else "FAIL")
