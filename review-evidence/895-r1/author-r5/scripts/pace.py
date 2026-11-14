#!/usr/bin/env python3
"""pace.py TREE [POINT]: the tree's pace and THE TRANSMIT's figures against the model's, read-only on TREE: the stated
AECP_PACE_MS, CTRL_LOOP_TX_BOUND_MS and CTRL_LOOP_TX_MS at POINT (default 1x1/1if), paced_rows.choice, and the tx, txL
and R4L rows of the built design at each pace from 1 to paced_rows.PACE_MOST_MS (rows_tiers.solve, paced_rows.r4l
through solve), then paced_rows.statements and rows_tiers.tx_statements at both points."""
import math
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
point = sys.argv[2] if len(sys.argv) > 2 else '1x1/1if'
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import paced_rows  # noqa: E402
import rows_tiers as rt  # noqa: E402

i = rt.point_inputs(root, point)
print(f'{point}: AECP_PACE_MS {i.pace_ms}, CTRL_LOOP_TX_BOUND_MS {i.tx_bound}, CTRL_LOOP_TX_MS {i.tx_stated}')
print(f'model choice (1x1/1if): {paced_rows.choice(root)}')
for p in range(1, paced_rows.PACE_MOST_MS + 1):
    at = i._replace(pace_ms=p)
    tx, txl, r4l = (rt.solve(row, at, rt.BUILT)[0] for row in ('tx', 'txL', 'R4L'))
    print(f'P {p:2d}: tx {tx} (ceil {math.ceil(tx - 1e-9) if tx else None}) txL {txl} R4L {r4l}')
print('paced_rows.statements:', paced_rows.statements(root))
print('rows_tiers.tx_statements:', rt.tx_statements(root))
