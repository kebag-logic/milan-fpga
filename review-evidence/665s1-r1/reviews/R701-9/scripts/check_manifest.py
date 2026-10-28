"""Check downloaded evidence files against the evidence tree's MANIFEST.json published_sha256.

Usage: check_manifest.py MANIFEST_JSON EVIDENCE_ROOT PREFIX
EVIDENCE_ROOT holds files downloaded from <PREFIX>/...; every file there must be listed and match.
"""
import hashlib
import json
import sys
from pathlib import Path

manifest, root, prefix = json.load(open(sys.argv[1])), Path(sys.argv[2]), sys.argv[3].rstrip('/') + '/'
listed = {e['file']: e['published_sha256'] for e in manifest}
ok = bad = missing = 0
for path in sorted(p for p in root.rglob('*') if p.is_file()):
    key = prefix + str(path.relative_to(root))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if key not in listed:
        missing += 1
        print('UNLISTED', key)
    elif listed[key] != digest:
        bad += 1
        print('MISMATCH', key)
    else:
        ok += 1
print(f'manifest entries {len(listed)}; checked {ok} match, {bad} mismatch, {missing} unlisted')
sys.exit(1 if bad or missing else 0)
