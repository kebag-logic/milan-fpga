#!/usr/bin/env python3
"""Every author/MANIFEST.sha256 mismatch must be an archiver path redaction
whose recorded original hash equals the manifest entry and whose published
hash equals the file on the branch. usage: check_redaction_map.py <b3-r1 dir>"""
import hashlib, json, sys
from pathlib import Path
ev = Path(sys.argv[1]); sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
arch = {e['file']: e for e in json.loads((ev / 'MANIFEST.json').read_text())}
bad = n = 0
for line in (ev / 'author/MANIFEST.sha256').read_text().splitlines():
    h, p = line.split(None, 1); f = ev / 'author' / p
    got = sha(f)
    if got != h:
        e = arch.get('author/' + p); n += 1
        ok = e and e['path_redacted'] and e['original_sha256'] == h and e['published_sha256'] == got
        bad += not ok
        print(f'{p}: manifest {h[:12]} published {got[:12]} archiver original {e and e["original_sha256"][:12]} redacted={e and e["path_redacted"]} {"EXPLAINED" if ok else "UNEXPLAINED"}')
red = [k for k, e in arch.items() if e['path_redacted'] and k.startswith('author/')]
print(f'mismatches {n}; archiver path-redacted author files {len(red)}: {red}')
lines = (ev / 'author/runs/din-long/events.jsonl').read_text().splitlines()
print('pattern-period record:', lines[0])
sys.exit(1 if bad else 0)
