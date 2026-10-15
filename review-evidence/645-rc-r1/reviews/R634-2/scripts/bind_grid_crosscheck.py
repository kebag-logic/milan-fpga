#!/usr/bin/env python3
"""Independent cross-check of a follow_ring bind sweep pair (head, dev datapath).

usage: bind_grid_crosscheck.py <head dir> <base dir>
Classes every bind by the head run's window label, then tabulates, per class, the
head's and the dev datapath's SLIP_LB outcome and slip events (kind, time after
the bind, time from the first burst). Also: every head slip before the ring acts
(head 'frames N before'), and whether the same run/cycle on dev shows a slip of
the same kind at the same time to the microsecond.
"""
import collections, re, sys
from pathlib import Path
res = re.compile(r"RESULT-645-BIND: B17 cycle (\d+) phase ([0-9.]+) at INTERNAL: first PDU \+([0-9.]+) ms after the bind, "
                 r"primed margin ([-0-9.e+]+)\.\.([-0-9.e+]+) us \((inside|OUTSIDE) B17's window\), arms (\d+).*?settle recentres (\d+)"
                 r".*?render recentres (\d+), SLIP_LB \+(\d+) dups \+(\d+) skips, slipped frames (\d+) before the ring acts and (\d+) after")
sl = re.compile(r"info: B17 cycle (\d+): slip \((dup|skip)\) ([-+0-9.]+) s after the bind, ([-+0-9.]+) s from")
def read(d):
    out, rcs = {}, {}
    for log in sorted(Path(d).glob('bind_*.log')):
        rcs[log.stem] = (Path(d) / (log.stem + '.rc')).read_text().strip()
        cur = None
        for line in log.read_text().splitlines():
            m = res.search(line)
            if m:
                g = m.groups(); cur = (log.stem, int(g[0]))
                assert cur not in out
                out[cur] = dict(phase=float(g[1]), plo=float(g[3]), phi=float(g[4]), win=g[5], ars=(g[6], g[7], g[8]),
                                dups=int(g[9]), skips=int(g[10]), pre=int(g[11]), post=int(g[12]), slips=[])
                continue
            m = sl.search(line)
            if m and cur and int(m.group(1)) == cur[1]:
                out[cur]['slips'].append((m.group(2), m.group(3), float(m.group(4))))
    return out, rcs
head, hrc = read(sys.argv[1]); base, brc = read(sys.argv[2])
assert set(head) == set(base), 'bind sets differ'
print('runs head', len(hrc), 'rc0', sum(v == '0' for v in hrc.values()), '| base', len(brc), 'rc0', sum(v == '0' for v in brc.values()))
print('binds', len(head))
for cls in ('inside', 'OUTSIDE'):
    ks = [k for k in head if head[k]['win'] == cls]
    hc = collections.Counter((head[k]['dups'], head[k]['skips'], head[k]['pre'], head[k]['post']) for k in ks)
    bc = collections.Counter((base[k]['dups'], base[k]['skips'], len(base[k]['slips'])) for k in ks)
    print(f'{cls}: {len(ks)} (head labels); dev labels inside among them: {sum(base[k]["win"] == "inside" for k in ks)}')
    print('  head (dups, skips, frames before, frames after):', dict(sorted(hc.items())))
    print('  dev  (dups, skips, slip events):', dict(sorted(bc.items())))
    print('  head arms/settle/render all 1:', sum(head[k]['ars'] == ('1', '1', '1') for k in ks), ' dev all 0:', sum(base[k]['ars'] == ('0', '0', '0') for k in ks))
    if cls == 'inside':
        ok = [k for k in ks if base[k]['dups'] == 2 and base[k]['skips'] == 0 and len(base[k]['slips']) == 1 and 0 <= base[k]['slips'][0][2] < 0.01]
        print('  dev exactly one frame at its first burst, nothing else:', len(ok))
        lo = min(head[k]['plo'] for k in ks); hi = max(head[k]['phi'] for k in ks)
        print(f'  head primed range over inside binds {lo:.3f}..{hi:.3f} us')
        for k in ks:
            if not (base[k]['dups'] == 2 and len(base[k]['slips']) == 1 and 0 <= base[k]['slips'][0][2] < 0.01):
                print('   dev other:', k, base[k]['dups'], base[k]['skips'], base[k]['slips'])
early = [(k, s) for k in head for s in head[k]['slips'] if s[2] < 0]
print('head slips before the first burst:', len(early), 'binds', len({k for k, _ in early}))
same = 0
for k, s in early:
    if any(b[0] == s[0] and b[1] == s[1] for b in base[k]['slips']):
        same += 1
    else:
        print('   NOT on dev identically:', k, s, base[k]['slips'])
print('identical on dev (kind and time-after-bind string):', same, 'of', len(early))
post = sum(head[k]['post'] for k in head)
print('head frames after the ring acts:', post)
moved = sorted({k[0] for k in head if head[k]['win'] == 'inside' and min(head[k]['plo'], 99) < 10.0})
print('head inside binds with primed low edge < 10 us:', sum(1 for k in head if head[k]['win'] == 'inside' and head[k]['plo'] < 10.0), moved)
