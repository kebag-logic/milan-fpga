#!/usr/bin/env python3
"""THE PACE's table at 1x1/1if under the built design: txL and R4L at each whole pace from 1 to PACE_MOST_MS, against
the derived bounds (rows_tiers.TX_BUDGET_MS, paced_rows.PACED_BOUNDS), with the model's choice and the tree's
statements. usage: python3 -I pace_table.py TREE"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import paced_rows  # noqa: E402
import rows_tiers as rt  # noqa: E402

head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=no'], capture_output=True,
                       text=True).stdout.strip().splitlines()
i = rt.point_inputs(root, '1x1/1if')
r4l = paced_rows.PACED_BOUNDS['R4L']
print(f'# THE PACE at {head} ({len(dirty)} changed paths), 1x1/1if, the built design: the tree states AECP_PACE_MS '
      f'{i.pace_ms}, slice {i.slice_us} us, record.aecp.long {i.c.get("record.aecp.long")} us; txL bound '
      f'{i.tx_bound} ms, R4L bound {r4l} ms')
print(f'| P, ms | txL, ms ({i.tx_bound}) | R4L, ms ({r4l}) | holds both |')
print('|---:|---:|---:|---|')
for pace in range(1, paced_rows.PACE_MOST_MS + 1):
    at = i._replace(pace_ms=pace)
    tx, r4 = rt.solve('txL', at, rt.BUILT)[0], rt.solve('R4L', at, rt.BUILT)[0]
    held = tx is not None and tx <= i.tx_bound and r4 is not None and r4 <= r4l
    print(f"| {pace} | {tx} | {r4} | {'yes' if held else 'no'} |")
print(f'paced_rows.choice: {paced_rows.choice(root)}  statements (tree against model): '
      f"{paced_rows.statements(root) or 'none'}")
print(f'slice_choice: {rt.slice_choice(root)}  ruled(): {rt.ruled(root)}')
