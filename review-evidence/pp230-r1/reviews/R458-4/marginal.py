#!/usr/bin/env python3
"""Re-derive 10 sec 5.1's per-context cost ((8x8 - 1x1) / 7) from the published
standalone hierarchy reports. Usage: marginal.py <dir with {base,head}/ooc-{1x1,8x8}/baseline_hierarchy.rpt>"""
import re, sys, os
root = sys.argv[1]
def rows(p):
    out, ind = {}, None
    for line in open(p):
        c = line.split('|')
        if len(c) < 9:
            continue
        name = c[1].strip()
        depth = len(c[1]) - len(c[1].lstrip())
        if name == 'u_srp':
            ind = depth
        elif ind is not None and depth <= ind:
            ind = None
        if name in ('u_srp', 'u_talker', 'u_listener', 'u_admission') and (
                name == 'u_srp' or ind is not None):
            out.setdefault(name, (int(c[3]), int(c[7])))
    return out
for side in ('base', 'head'):
    a = rows(os.path.join(root, side, 'ooc-1x1', 'baseline_hierarchy.rpt'))
    b = rows(os.path.join(root, side, 'ooc-8x8', 'baseline_hierarchy.rpt'))
    for k in ('u_talker', 'u_listener', 'u_admission', 'u_srp'):
        print(side, k, '1x1', a[k], '8x8', b[k],
              'per-context LUT %.1f FF %.1f' % ((b[k][0]-a[k][0])/7, (b[k][1]-a[k][1])/7))
