#!/usr/bin/env python3
"""verify_manifest.py MANIFEST.json LOCAL=REMOTE_PATH... : compare local downloads with the
published manifest's sha256 entries (paths relative to review-evidence/pp203-r1)."""
import hashlib, json, sys
man = {e["file"]: e for e in json.load(open(sys.argv[1]))}
bad = 0
for arg in sys.argv[2:]:
    loc, rem = arg.split("=", 1)
    h = hashlib.sha256(open(loc, "rb").read()).hexdigest()
    e = man.get(rem)
    ok = e is not None and e["published_sha256"] == h
    bad += not ok
    print(f"{'OK  ' if ok else 'BAD '} {rem} {h[:16]} manifest={e['published_sha256'][:16] if e else 'ABSENT'}")
print(f"{len(sys.argv)-2-bad} of {len(sys.argv)-2} match"); sys.exit(bad != 0)
