"""The heaviest poll item of each kind over a leg's finished group logs (poll_grade.held, the harness's own measure).
usage: python3 -I acmp_item.py HARNESS_DIR N_IF LOG..."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import grade, poll_grade
n_if = int(sys.argv[2])
best = {}
for f in sys.argv[3:]:
    t = Path(f).read_text(errors='replace')
    if 'SUMMARY' not in t[-4000:]:
        continue
    h = poll_grade.held(grade.parse(t, 100_000_000, 100_000_000), n_if)
    for k, v in h['heaviest'].items():
        if v > best.get(k, (0, ''))[0]:
            best[k] = (v, Path(f).parent.name + '/' + Path(f).name)
for k, (v, g) in sorted(best.items()):
    print(f'{k:10s} {v:>8,} cycles  {g}')
