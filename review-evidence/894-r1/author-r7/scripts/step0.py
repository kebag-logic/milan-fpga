"""STEP 0 (#894 ruling issuecomment-6857835707, item 3): the model what-if of txL and the last queued notice at
1x1/1if under the built design, for P = 8 to 11, the polls' base at 155, 180 and 205 us and ACMP's item at 35, 80
and 125 us. Every other input is the tree's (rows_tiers.point_inputs: the pin column the flip check reads).

Usage: python3 -I step0.py <tree root>. Read only; prints a markdown table and the combinations holding both rows.
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
b = rt.bounds_at(i._replace(pace_ms=8))
print(f'# STEP 0 at {head}, 1x1/1if, the built design; the tree: AECP_PACE_MS {i.pace_ms}, slice {i.slice_us} us, '
      f"base {i.c['base']} us, item.acmp {i.c['item.acmp']} us, record.aecp.long {i.c['record.aecp.long']} us")
tree = {r: rt.solve(r, i, rt.BUILT)[0] for r in ('txL', 'last', 'R4L')}
print(f'# the tree as is: txL {tree["txL"]}, last {tree["last"]}, R4L {tree["R4L"]}')
print(f"# bounds: txL {b['txL']} ms, last {b['last']} ms, R4L {b['R4L']} ms (paced)")
print('| P, ms | base, us | ACMP item, us | txL, ms (40) | last, ms (125) | R4L, ms (240) | txL and last hold | '
      'and R4L |')
print('|---:|---:|---:|---:|---:|---:|---|---|')
held = []
for pace in range(8, 12):
    for base in (155, 180, 205):
        for acmp in (35, 80, 125):
            at = i._replace(pace_ms=pace, c={**i.c, 'base': base, 'item.acmp': acmp})
            tx, last, r4l = (rt.solve(r, at, rt.BUILT)[0] for r in ('txL', 'last', 'R4L'))
            both = tx is not None and tx <= b['txL'] and last is not None and last <= b['last']
            r4 = r4l is not None and r4l <= paced_rows.RESPONSE_MS
            if both:
                held.append((pace, base, acmp, tx, last, r4l, r4))
            print(f"| {pace} | {base} | {acmp} | {tx:.2f} | {last:.2f} | {r4l:.2f} | {'yes' if both else 'no'} | "
                  f"{'yes' if both and r4 else 'no'} |")
print()
print(f'# combinations holding txL and the last queued notice: {len(held)} of 36')
for pace, base, acmp, tx, last, r4l, r4 in held:
    print(f'#   P {pace}, base {base}, ACMP item {acmp}: txL {tx:.2f}, last {last:.2f}, R4L {r4l:.2f}'
          f"{'' if r4 else ' (R4L over 240)'}")
