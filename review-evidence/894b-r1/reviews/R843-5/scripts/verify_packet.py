#!/usr/bin/env python3
"""Reviewer check: every file of the author packets author-r8..author-r12 in the evidence archive matches the
archive's MANIFEST.json published_sha256, and no file is present that the manifest does not list.
usage: verify_packet.py EXTRACTED_894b-r1_DIR MANIFEST.json"""
import hashlib, json, os, sys
base, manifest = sys.argv[1], json.load(open(sys.argv[2]))
rounds = tuple(f'author-r{r}/' for r in (8, 9, 10, 11, 12))
listed, ok, bad, missing = set(), 0, [], []
for e in manifest:
    if not e['file'].startswith(rounds):
        continue
    listed.add(e['file']); p = os.path.join(base, e['file'])
    if not os.path.exists(p):
        missing.append(e['file']); continue
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() == e['published_sha256']:
        ok += 1
    else:
        bad.append(e['file'])
present = {os.path.relpath(os.path.join(d, f), base) for r in rounds for d, _, fs in os.walk(os.path.join(base, r))
           for f in fs}
print(f'listed {len(listed)}, matching {ok}, mismatched {len(bad)}, missing {len(missing)}, unlisted {len(present - listed)}')
for f in bad + missing + sorted(present - listed):
    print('  ', f)
sys.exit(0 if not (bad or missing or present - listed) else 1)
