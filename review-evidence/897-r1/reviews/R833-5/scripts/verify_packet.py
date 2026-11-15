#!/usr/bin/env python3
"""Check an author packet against its own INDEX.md and the archive's MANIFEST.json.

usage: python3 -I verify_packet.py ARCHIVE_DIR PACKET   (ARCHIVE_DIR is review-evidence/897-r1; PACKET e.g. author-r5)
Every INDEX row must be present; its bytes must match the INDEX hash, or, for a file the manifest records as
path_redacted, the manifest's published hash, with the manifest's original hash equal to the INDEX row."""
import hashlib
import json
import re
import sys
from pathlib import Path

root, packet = Path(sys.argv[1]), sys.argv[2]
manifest = {e['file']: e for e in json.loads((root / 'MANIFEST.json').read_text())}
rows = {}
for line in (root / packet / 'INDEX.md').read_text().splitlines():
    m = re.match(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|', line)
    if m:
        rows[f'{packet}/{m[1]}'] = m[3]
bad, redacted, missing = [], [], []
for name, want in rows.items():
    p = root / name
    if not p.is_file():
        missing.append(name)
        continue
    have = hashlib.sha256(p.read_bytes()).hexdigest()
    e = manifest.get(name)
    if have == want:
        continue
    if e and e.get('path_redacted') and e['published_sha256'] == have and e['original_sha256'] == want:
        redacted.append(name)
    else:
        bad.append(name)
in_packet = [k for k in manifest if k.startswith(packet + '/')]
pub_bad = [k for k in in_packet if hashlib.sha256((root / k).read_bytes()).hexdigest() != manifest[k]['published_sha256']]
print(f'{packet}: {len(rows)} INDEX rows; {len(missing)} missing; {len(bad)} mismatched; '
      f'{len(redacted)} differ only by a recorded path redaction: {redacted}')
print(f'{packet}: {len(in_packet)} manifest entries; {len(pub_bad)} not matching their published hash; '
      f'{sum(1 for k in in_packet if manifest[k].get("path_redacted"))} recorded as path-redacted')
sys.exit(1 if missing or bad or pub_bad else 0)
