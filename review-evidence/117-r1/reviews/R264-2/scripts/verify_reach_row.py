#!/usr/bin/env python3
"""Box 1 'reaches asCapable' row: for each step 3 cycle, the first console
sample with CLKV_STAT[16]=1 after the outage, the completion times of the
DUT-initiated Pdelay exchanges with the switch after the link returned, and
PDELAY_NS at that sample.

usage: verify_reach_row.py A202_BENCH_DIR
"""
import sys, os, struct, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'rederive_step3.py')).read().split('\npage_rows = {')[0]
ns = {'__name__': 's3'}
argv = sys.argv
sys.argv = ['x', 'unused']
exec(compile(src, 'rederive_step3.py', 'exec'), ns)
sys.argv = argv
bench = sys.argv[1]
for c in range(1, 7):
    cdir = os.path.join(bench, 'cycle%d' % c)
    ofs = ns['offsets'](cdir)
    pw = ns['power'](cdir)
    t_off = pw['T_OFF_CMD'] - ofs['strip']
    S = ns['console'](cdir)
    for s in S:
        s['r'] = s['t'] - t_off
    asc0 = next(s['r'] for s in S if s['r'] > 0 and s['asc'] == '0')
    i = next(i for i, s in enumerate(S) if s['r'] > asc0 and s['asc'] == '1')
    asc1, prev, pd = S[i]['r'], S[i - 1]['r'], S[i]['pdelay']
    # decode DUT-initiated exchanges with sequence ids
    raw = open(os.path.join(cdir, 'tap-c%d.pcap' % c), 'rb').read()
    fr, _r, _n = ns['tap'](os.path.join(cdir, 'tap-c%d.pcap' % c))
    fr = [(t - ofs['capture'] - t_off, port, k, inf) for t, port, k, inf in fr]
    sw_first = next(x[0] for x in fr if x[1] == 2 and x[0] > 30)
    # completions: switch Pdelay_Resp_Follow_Up (port 2, PRFU) after the return
    prfu = [x[0] for x in fr if x[1] == 2 and x[2] == 'PRFU' and x[0] > sw_first - 0.001]
    second = prfu[1]
    print('cycle %d: asCapable 1 first seen %.3f (previous sample %.3f); 2nd DUT exchange completed %.3f; '
          'asc1 - second %.3f s; asc1 - switch first frame %.2f s; PDELAY_NS %s' % (
              c, asc1, prev, second, asc1 - second, asc1 - sw_first, pd))
