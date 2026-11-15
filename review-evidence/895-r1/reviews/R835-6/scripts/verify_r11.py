#!/usr/bin/env python3
"""verify_r11.py PACKET_DIR MANIFEST_JSON

Reviewer check of a published author packet: every row of PACKET_DIR/receipts/INDEX.md (file, bytes, sha256, per
section) against the file's bytes; every file under receipts/ listed; and every file under PACKET_DIR against the
archive MANIFEST.json's published_sha256 (entries whose 'file' starts with PACKET_DIR's name). Read-only.
Exit 1 on any mismatch."""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

pkt, man = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
rec = pkt / 'receipts'
bad = ok = 0
seen = set()
section = '.'
for line in (rec / 'INDEX.md').read_text().splitlines():
    m = re.match(r'## (.+)', line)
    if m:
        section = m.group(1).strip()
        continue
    m = re.match(r'\| (\S+) \| (\d+) \| `([0-9a-f]{64})` \|', line)
    if m:
        p = os.path.normpath(os.path.join(section, m.group(1)))
        seen.add(p)
        f = rec / p
        b = f.read_bytes() if f.is_file() else None
        if b is not None and len(b) == int(m.group(2)) and hashlib.sha256(b).hexdigest() == m.group(3):
            ok += 1
        else:
            bad += 1
            print('INDEX MISMATCH', p)
present = {str(p.relative_to(rec)) for p in rec.rglob('*') if p.is_file()} - {'INDEX.md'}
unlisted = sorted(present - seen)
print(f'INDEX rows verified {ok}, mismatched {bad}, unlisted files {len(unlisted)} {unlisted}')

entries = {e['file']: e['published_sha256'] for e in json.loads(man.read_text())
           if e['file'].startswith(pkt.name + '/')}
files = {f'{pkt.name}/{p.relative_to(pkt)}': p for p in pkt.rglob('*') if p.is_file()}
mok = mbad = 0
for name, p in sorted(files.items()):
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if entries.get(name) == h:
        mok += 1
    else:
        mbad += 1
        print('MANIFEST MISMATCH', name)
missing = sorted(set(entries) - set(files))
print(f'MANIFEST entries {len(entries)}, files {len(files)}, matched {mok}, mismatched {mbad}, '
      f'listed but absent {len(missing)}')
bad += mbad + len(unlisted) + len(missing)
print('RESULT', 'PASS' if bad == 0 else 'FAIL')
sys.exit(1 if bad else 0)
