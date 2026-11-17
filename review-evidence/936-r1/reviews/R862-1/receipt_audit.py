#!/usr/bin/env python3
"""Inspect the published receipts without treating summaries as new executions.
Run: python3 -B receipt_audit.py EXTRACTED_AUTHOR_RECEIPTS
"""
import hashlib
import json
from pathlib import Path
import re
import sys

p = Path(sys.argv[1])
def doc(relative):
    text = (p / relative).read_text()
    return text.split('\n\n', 1)[1] if text.startswith('Original file:') else text
def hashes(relative, exclude_elf=False):
    out = {}
    for line in doc(relative).splitlines():
        m = re.match(r'([0-9a-f]{64})\s+(.+)', line)
        if m and not (exclude_elf and m[2].endswith('/bios.elf')):
            out[m[2]] = m[1]
    assert out, relative
    return out

base = hashes('final/images/release-70f4056f-IMAGES.sha256', True)
head = hashes('final/head-7cfb8a04/images/rel-k-IMAGES.sha256', True)
assert base == head
print('Release base/final published hashes match:', len(base))
for kind, count in [('led', 24), ('fix', 6)]:
    prefix = 'final/head-7cfb8a04/images/'
    left, right = hashes(prefix + kind + '-j.sha256'), hashes(prefix + kind + '-k.sha256')
    assert left == right and len(left) == count
    print('b496c99e/final published', kind, 'hashes match:', len(left))

for name in ['1x1', '8x8-1if', 'vd-1x1', 'vd-8x8-1if', 'later-1x1', 'later-8x8-1if', 'every-1x1']:
    j = json.loads(doc('final/budget/' + name + '/results-summary.json'))
    print(json.dumps(dict(group=name, counts=j['counts'], refusals=j['refusals'], misses=j['misses'],
                          share_misses=j['share_misses'], notice_misses=j['notice_misses'],
                          notices=j['notices']['count'],
                          notice_max_ms=(j['notices']['longest'] or {}).get('ms')), sort_keys=True))
    assert not j['refusals'] and not j['share_misses'] and not j['notice_misses']
    assert len(j['misses']) == (7 if name in ['1x1', '8x8-1if'] else 0)

twin = doc('final/head-7cfb8a04/k-twin.log')
for needle in ['plant output-notice-dropped: REFUSED by "the fabric sent and the split did not:',
               'plant output-notice-dropped: REFUSED by "owed row stream-output-0-dest-mac does not hold"',
               'plant vanished-owed: REFUSED by "owed row stream-output-0-dest-mac: the difference has gone"',
               'TWIN-PLANTS-BUT-SRP-PLUS-K rc=0']:
    assert needle in twin, needle
    print('Published twin receipt contains:', needle)
print('PASS: receipt consistency; no target simulation executed by this audit')
