#!/usr/bin/env python3
"""Reproduce the evidence behind R575-1 findings F1-F4 from the archived packet and the head tree.
usage: check_findings.py <packet-root review-evidence/608-b14-r1> <repo checkout at the head>"""
import csv, json, re, sys
pk, repo = sys.argv[1], sys.argv[2]
a = pk + '/author'
doc = open(repo + '/docs/findings/B14_BENCH_5603C353.md').read().split('\n')
def line(pat):
    return [(i + 1, l) for i, l in enumerate(doc) if re.search(pat, l)]
print('== F1: DUT Talker Advertise Lv timing in cycles 2 and 42')
print('doc:', line(r'withdrawing its Talker Advertise'))
for c in (2, 42):
    d = '%s/item3/cycles/cycle-%03d' % (a, c)
    ms = list(csv.DictReader(open(d + '/msrp.tsv'), delimiter='\t'))
    ac = list(csv.DictReader(open(d + '/acmp.tsv'), delimiter='\t'))
    disc = next(float(x['t_s']) for x in ac if x['mt'] == '9')
    lv = next(float(x['t_s']) for x in ms if x['sender'] == 'bridge' and x['type'] == 'Listener' and x['event'] == 'Lv' and float(x['t_s']) >= disc)
    ta = next(float(x['t_s']) for x in ms if x['sender'] == 'DUT' and x['type'] == 'TalkerAdvertise' and x['event'] == 'Lv' and float(x['t_s']) >= disc)
    print('  cycle %d: DISCONNECT_RX response %.6f, bridge Lv %.6f, DUT TA Lv %.6f -> after bridge Lv %.4f s, after response %.4f s'
          % (c, disc, lv, ta, ta - lv, ta - disc))
print('== F2: soak capture-loss bursts per stream')
print('doc:', line(r'lose a burst'))
for l in open(a + '/soak/soak-overlap-recovery.txt'):
    print('  ', l.rstrip())
print('== F3: SLIP_LB around the soak binds (console 0x8D4, little-endian word)')
print('doc:', line(r'One loopback slip at INTERNAL'))
def slip(f):
    t = open(f).read()
    ts = re.search(r"### (\S+) cmd='mem_read 0x900008d4 12'", t).group(1)
    b = re.search(r'0x900008d4\s+((?:[0-9a-f]{2} ){4})', t).group(1).split()
    return ts, int(''.join(reversed(b)), 16)
for f in ('soak/console-prebind.txt', 'soak/console-soak-000.txt', 'soak/console-soak-005.txt', 'soak/console-soak-010.txt'):
    ts, v = slip(a + '/' + f)
    print('  %-28s %s SLIP_LB dups 0x%x' % (f, ts, v))
for f in ('soak/bind-a-aaf.jsonl', 'soak/bind-a-crf.jsonl'):
    for l in open(a + '/' + f):
        e = json.loads(l)
        if e['kind'] == 'bind':
            print('  bind %s -> %s at epoch %.3f' % (e['talker'], e['listener'], e['t']))
print('  soak t0 epoch (soak-coverage.txt):', open(a + '/soak/soak-coverage.txt').readline().split()[1])
print('== F4: RMON lanes and STATS_CAP')
print('doc:', line(r'RMON lanes hold'))
summ = json.load(open(a + '/soak/summary.json'))
cap = int(summ['console'][0]['rmon_0x200_0x230'][1], 16)
enum = [l.split()[0].rstrip(',').split('=')[0] for l in open(repo + '/hdl/common/eth_event_counter/ethernet_events.svh') if re.match(r'\s+(TX|RX)_\w+', l)]
for n, name in enumerate(enum):
    print('  lane %d 0x%03x %-20s STATS_CAP bit %d' % (n, 0x210 + 4 * n, name, cap >> n & 1))
rm = open(repo + '/docs/reference/REGISTER_MAP.md').read().split('\n')
print('  REGISTER_MAP:', [(i + 1, l[:110]) for i, l in enumerate(rm) if 'STAT_RX_FIFO_OVERFLOW' in l or l.startswith('| `RX_FIFO_OVERFLOW`')])
