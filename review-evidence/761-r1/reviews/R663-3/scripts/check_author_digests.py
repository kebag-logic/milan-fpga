#!/usr/bin/env python3
"""Compare downloaded author-r3 receipt copies with MANIFEST.json published_sha256.

Usage: check_author_digests.py <MANIFEST.json> <copies-dir>
A copy named a_b_c.ext maps to author-r3/receipts/a/b_c.ext (first '_' is the
directory separator, as written by the download step).
"""
import hashlib
import json
import pathlib
import sys

man = {e["file"]: e for e in json.load(open(sys.argv[1]))}
bad = 0
for p in sorted(pathlib.Path(sys.argv[2]).iterdir()):
    d, _, rest = p.name.partition("_")
    key = f"author-r3/receipts/{d}/{rest}"
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    e = man.get(key)
    if e is None:
        print(f"MISSING {key}")
        bad += 1
        continue
    ok = got == e["published_sha256"]
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {key} {got}")
print(f"result: {'PASS' if bad == 0 else 'FAIL'} ({bad} mismatches)")
sys.exit(1 if bad else 0)
