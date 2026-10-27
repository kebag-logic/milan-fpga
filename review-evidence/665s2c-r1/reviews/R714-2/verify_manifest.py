"""Check each published file under a prefix against the evidence tree's MANIFEST.json.

Usage: python3 -I verify_manifest.py <review-evidence/665s2c-r1 dir> <prefix>
"""
import hashlib
import json
import pathlib
import sys

root, prefix = pathlib.Path(sys.argv[1]), sys.argv[2]
entries = {e['file']: e for e in json.load(open(root / 'MANIFEST.json'))}
on_disk = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)).startswith(prefix)}
listed = {f for f in entries if f.startswith(prefix)}
bad = [f for f in sorted(on_disk & listed)
       if hashlib.sha256((root / f).read_bytes()).hexdigest() != entries[f]['published_sha256']]
print(f'{prefix}: listed {len(listed)}, on disk {len(on_disk)}, unlisted {sorted(on_disk - listed)}, '
      f'missing {len(listed - on_disk)}, hash mismatches {bad}')
