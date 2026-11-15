"""Verify an author round packet: every INDEX.md row (bytes, sha256), the outer MANIFEST.json's published_sha256 for the
round's files, and PR-BODY.md against a copy of the live PR body. Usage: verify_packet.py <archive-dir> <round-dir> <live-body>"""
import hashlib
import json
import re
import sys
from pathlib import Path
arch, rnd, live = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
n = bad = 0
for line in (arch / rnd / 'INDEX.md').read_text().splitlines():
    m = re.match(r"\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|", line)
    if m:
        n += 1
        b = (arch / rnd / m[1]).read_bytes()
        bad += hashlib.sha256(b).hexdigest() != m[3] or len(b) != int(m[2].replace(',', ''))
print(f'INDEX.md: {n} rows, {bad} mismatched')
k = badm = 0
for e in json.loads((arch / 'MANIFEST.json').read_text()):
    if e['file'].startswith(rnd + '/'):
        k += 1
        badm += hashlib.sha256((arch / e['file']).read_bytes()).hexdigest() != e['published_sha256']
print(f'MANIFEST.json: {k} entries for {rnd}, {badm} mismatched')
same = (arch / rnd / 'PR-BODY.md').read_bytes() == live.read_bytes()
print(f'PR-BODY.md identical to the live PR body: {same} (sha256 {hashlib.sha256(live.read_bytes()).hexdigest()})')
