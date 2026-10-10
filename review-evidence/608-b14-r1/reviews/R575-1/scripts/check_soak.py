#!/usr/bin/env python3
"""Recompute soak (item 5), item 6 and item 7 console figures from the archived soak records."""
import json, sys, re, collections, glob, os
pk = sys.argv[1]
s = pk + '/author/soak'
recs = [json.loads(l) for l in open(s + '/capture-receipts.jsonl')]
drops = collections.Counter(); rcs = collections.Counter(); recv_vs_capt = 0
for r in recs:
    rcs[r['rc']] += 1
    for line in r['summary']:
        m = re.search(r'(\d+) packets dropped by kernel', line)
        if m:
            drops[int(m.group(1))] += 1
print('capture receipts', len(recs), 'rc', dict(rcs), 'kernel drop values', dict(drops))
print('by filter', collections.Counter(r['capture'].rsplit('-', 1)[1] for r in recs))
# ledger
led = [l.rstrip('\n').split('\t') for l in open(s + '/ledger.tsv')]
print('ledger rows', len(led), 'verdicts', collections.Counter(x[3] for x in led), 'last elapsed', led[-1][2])
el = [float(x[2]) for x in led]
iv = [b - a for a, b in zip(el, el[1:])]
print('poll interval min/max', round(min(iv), 3), round(max(iv), 3))
# console reads
cons = sorted(glob.glob(s + '/console-*.txt'))
mac = collections.Counter(); rmon = collections.Counter(); maap = collections.Counter(); slip = []; syncs = collections.Counter()
for f in cons:
    t = open(f).read()
    for m in re.finditer(r'(?im)^.*?(0x0*8d4|SLIP_LB).*$', t):
        pass
    slip.append((os.path.basename(f), re.findall(r'[0-9a-fA-F]{8}', t)[:0]))
print('console files', len(cons))
summ = json.load(open(s + '/summary.json'))
c = summ['console']
print('summary console reads', len(c))
for r in c:
    mac[tuple(r['mac_status'])] += 1
    rmon[tuple(r['rmon_0x200_0x230'])] += 1
    maap[tuple(r['maap_0x6cc_0x6d4'])] += 1
    syncs[(r['sync_ascapable_tu'], r['gm_equals_parent'])] += 1
    slip.append((r['read'], r['utc'][11:19], r['slip_render_0x8d4_0x8dc']))
print('MAC_STATUS', dict(mac)); print('RMON 0x200..0x230', dict(rmon)); print('MAAP', dict(maap)); print('sync/gm', dict(syncs))
for x in slip:
    if isinstance(x[1], str):
        print('  slip/render', x)
d = summ['counter_deltas_first_to_last_poll']
ERR = {'MEDIA_UNLOCKED', 'STREAM_INTERRUPTED', 'SEQ_NUM_MISMATCH', 'UNSUPPORTED_FORMAT', 'LATE_TIMESTAMP', 'EARLY_TIMESTAMP',
       'STREAM_STOP', 'MEDIA_RESET', 'TIMESTAMP_UNCERTAIN', 'TIMESTAMP_NOT_VALID', 'LINK_DOWN', 'GPTP_GM_CHANGED', 'UNLOCKED'}
for k, v in d.items():
    if 'counters' in v:
        nz = {n: x['delta'] for n, x in v['counters'].items() if x['delta']}
        bad = {n: x for n, x in nz.items() if n in ERR}
        print(' ', k, 'nonzero deltas', nz, 'ERROR' if bad else '')
print('keys', [k for k in summ if k not in ('console', 'counter_deltas_first_to_last_poll')])
for k in ('t0_utc', 'polls', 'last_elapsed_s', 'chunks', 'polls_with_errors', 'timing_reads', 'timing_changes', 'hive_rule_increments'):
    print(k, summ.get(k))
