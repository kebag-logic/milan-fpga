#!/usr/bin/env python3
"""Decode item 2 GET_COUNTERS payloads (descriptor_type, index, counters_valid,
counter block) and grade each switch: which counters moved from 'before' to
'end', and whether DUT STREAM_INPUT MEDIA_UNLOCKED moved from 'locked' to 'end'
and from 'before' to 'end'. usage: check_item2_counters.py <packet-author-dir>"""
import collections, json, os, sys
A = sys.argv[1]
SI = ['MEDIA_LOCKED', 'MEDIA_UNLOCKED', 'STREAM_INTERRUPTED', 'SEQ_NUM_MISMATCH', 'MEDIA_RESET', 'TIMESTAMP_UNCERTAIN',
      'TIMESTAMP_VALID', 'TIMESTAMP_NOT_VALID', 'UNSUPPORTED_FORMAT', 'LATE_TIMESTAMP', 'EARLY_TIMESTAMP', 'FRAMES_RX']
SO = ['STREAM_START', 'STREAM_STOP', 'MEDIA_RESET', 'TIMESTAMP_UNCERTAIN', 'FRAMES_TX']
AI = ['LINK_UP', 'LINK_DOWN', 'FRAMES_TX', 'FRAMES_RX', 'RX_CRC_ERROR', 'GPTP_GM_CHANGED']
CD = ['LOCKED', 'UNLOCKED']
NAMES = {5: SI, 6: SO, 9: AI, 0x24: CD}
NOISE = {'FRAMES_RX', 'FRAMES_TX', 'TIMESTAMP_VALID'}
def dec(h):
    b = bytes.fromhex(h); dt = int.from_bytes(b[0:2], 'big'); valid = int.from_bytes(b[4:8], 'big')
    out = {}
    for i, n in enumerate(NAMES[dt]):
        if valid >> i & 1: out[n] = int.from_bytes(b[8 + 4 * i:12 + 4 * i], 'big')
    return out
marks = {}
for run in sorted(d for d in os.listdir(os.path.join(A, 'item2')) if d.startswith('cyc')):
    for l in open(os.path.join(A, 'item2', run, 'events.jsonl')):
        e = json.loads(l)
        if e['kind'] == 'counters':
            marks[e['tag']] = {k: dec(v) for k, v in e['payloads'].items()}
sw = sorted({t.rsplit('-', 1)[0] for t in marks})
moved_summary = collections.Counter(); mu_bad = []
for s in sw:
    b, en = marks.get(s + '-before'), marks.get(s + '-end'); lk = marks.get(s + '-locked')
    mv = {}
    for d in b:
        for n, v in b[d].items():
            dv = en[d][n] - v
            if dv and n not in NOISE: mv['%s.%s' % (d, n)] = dv
    moved_summary[tuple(sorted(mv.items()))] += 1
    for d in ('dut-0x0005-0', 'dut-0x0005-1'):
        mu_be = en[d]['MEDIA_UNLOCKED'] - b[d]['MEDIA_UNLOCKED']
        mu_le = en[d]['MEDIA_UNLOCKED'] - lk[d]['MEDIA_UNLOCKED'] if lk else None
        if mu_be or mu_le: mu_bad.append((s, d, mu_be, mu_le))
    print(s, 'non-noise moves before->end:', mv)
print('distinct move patterns:', len(moved_summary))
print('DUT STREAM_INPUT MEDIA_UNLOCKED moves (switch, desc, before->end, locked->end):', mu_bad)
