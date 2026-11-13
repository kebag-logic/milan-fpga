"""THE PACE's sweep at 1x1/1if under the built design: txL and R4L at each whole pace from 0 to PACE_MOST_MS.

Usage: python3 -B pace_sweep.py <tree root>. Read only; it prints a table, the model's choice, the tree's statements
and the slice rule's pick, as pace-choice.txt records them.
"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import paced_rows  # noqa: E402
import rows_tiers as rt  # noqa: E402

head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
i = rt.point_inputs(root, '1x1/1if')
print(f'# THE PACE at the head {head}, 1x1/1if, the built design: the tree states AECP_PACE_MS {i.pace_ms}, '
      f'slice {i.slice_us} us, record.aecp.long {i.c.get("record.aecp.long")} us')
print('| P, ms | txL, ms (40) | R4L, ms (240) | holds both |')
print('|---:|---:|---:|---|')
for pace in range(0, paced_rows.PACE_MOST_MS + 1):
    at = i._replace(pace_ms=pace)
    tx, r4 = rt.solve('txL', at, rt.BUILT)[0], rt.solve('R4L', at, rt.BUILT)[0]
    bound = paced_rows.RESPONSE_MS if pace else 20
    held = tx is not None and tx <= i.tx_bound and r4 is not None and r4 <= bound
    print(f"| {pace} | {tx} | {r4} | {'yes' if held else 'no'} |")
print('P = 0 is no pace: R4L is then held at 20 ms')
print(f'paced_rows.choice: {paced_rows.choice(root)}  statements (tree against model): '
      f"{paced_rows.statements(root) or 'none'}")
print(f'slice_choice: {rt.slice_choice(root)}  ruled(): {rt.ruled(root)}')
