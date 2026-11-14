#!/usr/bin/env python3
"""Verify every MANIFEST.json entry under the given prefixes against published bytes; list unlisted files."""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1]); prefixes = sys.argv[2:]
m = json.loads((root / 'MANIFEST.json').read_text())
listed = {e['file']: e for e in m if any(e['file'].startswith(p) for p in prefixes)}
bad = 0
for f, e in sorted(listed.items()):
    p = root / f
    if not p.is_file():
        print('MISSING', f); bad += 1; continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != e['published_sha256']:
        print('MISMATCH', f); bad += 1
present = {str(p.relative_to(root)) for pre in prefixes for p in (root / pre).rglob('*') if p.is_file()}
for f in sorted(present - set(listed)):
    print('UNLISTED', f)
red = sum(1 for e in listed.values() if e.get('path_redacted'))
print(f'listed {len(listed)} present {len(present)} bad {bad} unlisted {len(present-set(listed))} path_redacted {red}')
sys.exit(1 if bad else 0)
