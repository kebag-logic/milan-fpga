#!/usr/bin/env python3
"""R575-2: rebuild the SLIP_LB ledger (frames = dups / 2) from the archived packet.
Usage: check_slip_lb_ledger.py <author dir>"""
import json, os, re, sys, glob
a = sys.argv[1]
def slip(path):
    """(timestamp, SLIP_LB, rails) of each 0x900008d4 read in a console transcript."""
    out = []; ts = None; txt = open(path).read().split('\n')
    for i, l in enumerate(txt):
        m = re.match(r"### (\S+) cmd='mem_read 0x900008d4", l)
        if m: ts = m.group(1)
        m = re.match(r'0x900008d4\s+((?:[0-9a-f]{2} ){12})', l)
        if m and ts:
            b = bytes.fromhex(m.group(1).replace(' ', ''))
            out.append((ts, int.from_bytes(b[0:4], 'little'), (int.from_bytes(b[8:12], 'little') >> 16) & 0xff))
            ts = None
    return out
ph = json.load(open(os.path.join(a, 'item2/summary/switches.json')))
asf = slip(os.path.join(a, 'item2/setup/dut-before.txt')) + slip(os.path.join(a, 'item2/setup2/dut-before.txt'))
print('as found', asf)
first = ph[0]['slip_lb_before'][0]
L = {'setup to first set': first - asf[-1][1]}
aaf_tr = aaf_after = crf = intr = within_cycle = between_cycles = between_runs = 0
bc = []; br = []; wc = []
for i, p in enumerate(ph):
    k = p['tag'].split('-')[1]
    d = p['slip_lb_end'][0] - p['slip_lb_before'][0]
    if k == 'aaf':
        aaf_tr += p['slip_lb_boundary'][0] - p['slip_lb_before'][0]; aaf_after += p['slip_lb_end'][0] - p['slip_lb_boundary'][0]
    elif k == 'crf': crf += d
    else: intr += d
    if i:
        q = ph[i - 1]; g = p['slip_lb_before'][0] - q['slip_lb_end'][0]
        if q['run'] != p['run']: br.append((q['tag'], p['tag'], g))
        elif q['tag'].endswith('-int'): bc.append((q['tag'], p['tag'], g))
        else: wc.append((q['tag'], p['tag'], g))
L['INTERNAL->AAF, before boundary'] = aaf_tr; L['INTERNAL->AAF, after boundary'] = aaf_after
L['AAF->CRF holds'] = crf; L['returns to INTERNAL holds'] = intr
L['within a cycle, between phases'] = sum(g for *_, g in wc)
L['between the two cycles of a run'] = sum(g for *_, g in bc); L['between runs'] = sum(g for *_, g in br)
td = slip(os.path.join(a, 'item2/teardown/dut-after.txt'))
L['last poll to teardown read'] = td[-1][1] - ph[-1]['slip_lb_end'][0]
pre = slip(os.path.join(a, 'soak/console-prebind.txt'))
L['items 3 and 4 (teardown to prebind)'] = pre[-1][1] - td[-1][1]
soak = []
for f in sorted(glob.glob(os.path.join(a, 'soak/console-soak-*.txt'))): soak += slip(f)
fin = slip(os.path.join(a, 'restore/console-final.txt'))
L['across the soak bind (prebind to soak-000)'] = soak[0][1] - pre[-1][1]
steps = [(soak[i - 1][0], soak[i][0], soak[i][1] - soak[i - 1][1]) for i in range(1, len(soak)) if soak[i][1] != soak[i - 1][1]]
L['within the soak reads'] = soak[-1][1] - soak[0][1]
L['last soak read to final'] = fin[-1][1] - soak[-1][1]
print('between cycles', bc); print('between runs', br); print('within cycle', wc)
print('soak steps', steps, 'soak reads', len(soak), 'rails', sorted(set(r for *_, r in soak)))
print('teardown', td, 'prebind', pre, 'final', fin)
tot = 0
for k, v in L.items():
    print(f'{k:45s} dups {v:4d} frames {v / 2:5.1f}'); tot += v
print('total dups', tot, 'final', hex(fin[-1][1]), 'frames', tot / 2, 'consistent', tot == fin[-1][1] - asf[-1][1])
