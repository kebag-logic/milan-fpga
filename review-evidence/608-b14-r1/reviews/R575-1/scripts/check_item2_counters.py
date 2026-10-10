#!/usr/bin/env python3
"""Recompute item 2 counter deltas from the raw GET_COUNTERS payloads in item2/cycNN/events.jsonl."""
import json, sys, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from counters_lib import decode, delta
pk = sys.argv[1]
TRAFFIC = {'FRAMES_RX', 'FRAMES_TX', 'TIMESTAMP_VALID'}
for f in sorted(glob.glob(pk + '/author/item2/cyc*/events.jsonl')):
    snaps = {}
    for l in open(f):
        e = json.loads(l)
        if e['kind'] == 'counters':
            snaps[e['tag']] = {k: decode(v)[3] for k, v in e['payloads'].items()}
    phases = sorted({t.rsplit('-', 1)[0] for t in snaps})
    for ph in phases:
        first = snaps.get(ph + '-before') or snaps.get(ph + '-mid')
        end = snaps[ph + '-end']
        locked = snaps.get(ph + '-locked')
        nontraffic = {}
        for dev in end:
            d = {k: v for k, v in delta(first[dev], end[dev]).items() if k not in TRAFFIC}
            if d:
                nontraffic[dev] = d
        ltoe = {}
        if locked:
            for dev in end:
                d = {k: v for k, v in delta(locked[dev], end[dev]).items() if k not in TRAFFIC}
                if d:
                    ltoe[dev] = d
        print(ph, 'first->end', nontraffic, '| locked->end', ltoe)
