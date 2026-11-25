#!/usr/bin/env python3
"""Usage: python3 spotcheck_outputs.py PACKET. Match complete recorded outputs to log bytes."""
import hashlib
import json
from pathlib import Path
import sys

p = Path(sys.argv[1])
author = p/'scratch/review-evidence/cicd3-r1/author-r8/receipts/local'
expected = {}
for leg in (0, 1):
    for r in json.loads((author/f'fr-fr/{leg}.json').read_text())['results']:
        expected[r['case']] = r['output_sha256']
logs = [author/f'{side}/{leg}.log' for side in ('fr-old','fr-fr') for leg in (0,1)]
logs += [p/f'scratch/union-{run}/follow_ring.log' for run in (45550366428,45528738040)]
matches = []
for log in logs:
    raw = log.read_bytes()
    for case, digest in expected.items():
        marker = f'======== follow_ring/{case} ========\n'.encode()
        if marker not in raw:
            continue
        assert raw.count(marker) == 1
        tail = raw.split(marker)[1]
        # The union joins build logs between pieces. A recorded case digest must
        # match an exact prefix after its marker, ending on a line boundary.
        prefix = b''
        for line in tail.splitlines(keepends=True):
            prefix += line
            if hashlib.sha256(prefix).hexdigest() == digest:
                break
        else:
            raise AssertionError((str(log), case, digest))
        matches.append({'log':str(log.relative_to(p)), 'case':case, 'bytes':len(prefix), 'sha256':digest})
        if 'union-45550366428' in str(log):
            (p/f'follow-output-{case}.log').write_bytes(prefix)
assert len(matches) == 12, len(matches)
print(json.dumps(matches, indent=2))
print('PASS: 12 exact output hashes across prior/current local and hosted logs; all three cases identical')
