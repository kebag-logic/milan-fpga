"""Reviewer probe: the ruling's slice rule reproduced, every slice on the 50 us grid at 1x1/1if under the built
design's orders, each row's W and relative margin, the least, and the argmax; and the 8x8/2if rows at each slice.
usage: python3 -I slice_sweep.py <repo-root>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_tiers as rt  # noqa: E402
for point in ('1x1/1if', '8x8/2if'):
    i = rt.point_inputs(root, point)
    best = None
    print(point, 'smallest slice', rt.smallest_slice(i), 'DRAIN_US', i.h['CTRL_LOOP_DRAIN_US'])
    first = -(-rt.smallest_slice(i) // 50) * 50
    for us in range(first, i.h['CTRL_LOOP_DRAIN_US'] + 1, 50):
        r = rt.rows(root, point, rt.BUILT._replace(slice_us=us), i)
        m = rt.least_margin(r)
        cells = ' '.join(f'{k}={w:.2f}' if w is not None else f'{k}=none' for k, (w, _) in r.items())
        print(f'  {us:5d} us least {m:+.4f}  {cells}')
        if best is None or m > best[1]:
            best = (us, m)
    print('  argmax', best, 'rows_tiers.slice_choice', rt.slice_choice(root, point))
