"""Summarise milan_dp output-walk residuals (stamp - phc - offset) per leg, output and offset."""
import re, sys
leg = None
acc = {}
for l in open(sys.argv[1], errors='replace'):
    if 'obj_nxn8/Vmilan_dp_nxn8' in l and l.startswith('./'): leg = 'nxn8'
    elif 'obj_nxn/Vmilan_dp_nxn' in l and l.startswith('./'): leg = 'nxn'
    for m in re.finditer(r'timestamp output=(\d+) stamp=(\d+) phc=(\d+) offset=(\d+) residual=(-?\d+)', l):
        o, s, p, off, r = map(int, m.groups())
        k = (leg, o, off)
        lo, hi, n = acc.get(k, (r, r, 0))
        acc[k] = (min(lo, r), max(hi, r), n + 1)
for k in sorted(acc, key=str):
    print(k, 'min %d max %d n %d' % acc[k])
