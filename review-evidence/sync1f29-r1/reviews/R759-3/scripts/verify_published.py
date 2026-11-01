#!/usr/bin/env python3
"""verify_published.py MANIFEST_JSON NAME=PATH...: compare fetched evidence files with the published manifest's digests."""
import hashlib, json, sys
entries = {e['file']: e['published_sha256'] for e in json.load(open(sys.argv[1]))}
bad = 0
for arg in sys.argv[2:]:
    name, path = arg.split('=', 1)
    got = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    want = entries.get(name)
    ok = got == want
    bad += not ok
    print(f"{'ok' if ok else 'MISMATCH'} {name} {got}")
sys.exit(1 if bad else 0)
