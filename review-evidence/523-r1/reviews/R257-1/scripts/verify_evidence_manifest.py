#!/usr/bin/env python3
"""Verify a published evidence MANIFEST.json (file/published_sha256 rows)
against the files beside it. Usage: verify_evidence_manifest.py <dir>"""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]); m = json.load(open(root / 'MANIFEST.json'))
bad = [e['file'] for e in m if not (root / e['file']).is_file()
       or hashlib.sha256((root / e['file']).read_bytes()).hexdigest() != e['published_sha256']]
listed = {e['file'] for e in m}
present = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
unlisted = sorted(present - listed - {'MANIFEST.json'})
redacted = sum(1 for e in m if e['path_redacted'])
print('entries', len(m), 'bad', bad, 'unlisted', unlisted, 'path_redacted', redacted)
ok = not bad and not unlisted
print('MANIFEST', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
