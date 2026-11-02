#!/usr/bin/env python3
"""Check the published evidence tree against its MANIFEST.json and the author's receipts INDEX.md.

usage: verify_evidence.py <review-evidence/665s2b-r1>"""
import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
m = json.loads((root / 'MANIFEST.json').read_text())
print('manifest entries', len(m), 'sample', m[0] if isinstance(m[0], str) else {k: m[0][k] for k in list(m[0])[:4]})
ok = bad = absent = 0
for e in m:
    path, sha = e['file'], e['published_sha256']
    f = root / path if not str(path).startswith('review-evidence') else root.parents[1] / path
    if not f.exists():
        absent += 1
        continue
    if hashlib.sha256(f.read_bytes()).hexdigest() == sha: ok += 1
    else: bad += 1; print('DIFF', path)
print('manifest: ok', ok, 'different', bad, 'absent', absent)
ok = bad = absent = 0
base = root / 'author-r12/receipts'
for line in (base / 'INDEX.md').read_text().splitlines():
    g = re.match(r'\| `([^`]+)` \| [\d,]+ \| `([0-9a-f]{64})` \|', line)
    if not g: continue
    f = base / g.group(1)
    if not f.exists():
        absent += 1
        continue
    if hashlib.sha256(f.read_bytes()).hexdigest() == g.group(2): ok += 1
    else: bad += 1; print('DIFF', g.group(1))
print('author-r12 INDEX: ok', ok, 'different', bad, 'absent', absent)
