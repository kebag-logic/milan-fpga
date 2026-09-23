#!/usr/bin/env python3
"""Per step 3 capture: records without a tap envelope, and the dark window on
the DUT link (last record in either direction before the switch's return and
the first record after it), in seconds after the outlet-off command.

usage: verify_dark_window_hostrecs.py A202_BENCH_DIR
"""
import sys, os, struct
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'rederive_step3.py')).read().split('\npage_rows = {')[0]
ns = {'__name__': 's3'}
argv = sys.argv
sys.argv = ['x', 'unused']
exec(compile(src, 'rederive_step3.py', 'exec'), ns)
sys.argv = argv
bench = sys.argv[1]


def host_only(path):
    raw = open(path, 'rb').read()
    off, n = 24, 0
    while off + 16 <= len(raw):
        _s, _f, incl, _o = struct.unpack('<IIII', raw[off:off + 16])
        pkt = raw[off + 16:off + 16 + incl]
        off += 16 + incl
        if len(pkt) < 42 or struct.unpack('<I', pkt[:4])[0] != 6 or struct.unpack('<I', pkt[8:12])[0] not in (2, 3):
            n += 1
    return n


for c in range(1, 7):
    cdir = os.path.join(bench, 'cycle%d' % c)
    ofs = ns['offsets'](cdir)
    pw = ns['power'](cdir)
    t_off = pw['T_OFF_CMD'] - ofs['strip']
    p = os.path.join(cdir, 'tap-c%d.pcap' % c)
    fr, _r, _n = ns['tap'](p)
    fr = [(t - ofs['capture'] - t_off, port, k, i) for t, port, k, i in fr]
    gi = max(range(1, len(fr)), key=lambda i: fr[i][0] - fr[i - 1][0])
    last, first = fr[gi - 1], fr[gi]
    print('cycle %d: envelope-less records %d; dark from %.3f (%s, port %d) to %.3f (%s, port %d)' % (
        c, host_only(p), last[0], last[2], last[1], first[0], first[2], first[1]))
for rel in ('final/tap-final.pcap', 'attempt1-aborted/tap-c1.pcap'):
    print('%s: envelope-less records %d' % (rel, host_only(os.path.join(bench, rel))))
