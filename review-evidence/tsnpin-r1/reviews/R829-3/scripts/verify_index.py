#!/usr/bin/env python3
"""Check every row of a receipts INDEX.md (path | bytes | sha256 first 16) against the files under its directory.
Usage: python3 -I verify_index.py <receipts-dir>"""
import hashlib, os, re, sys
root = sys.argv[1]
rows = ok = bad = missing = 0
listed = set()
for line in open(os.path.join(root, "INDEX.md"), encoding="utf-8"):
    m = re.match(r"^\| `(.+)` \| ([\d,]+) \| `([0-9a-f]{16})` \|$", line.rstrip("\n"))
    if not m:
        continue
    rows += 1
    p, n, h = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
    listed.add(p)
    fp = os.path.join(root, p)
    if not os.path.isfile(fp):
        missing += 1; print("MISSING", p); continue
    data = open(fp, "rb").read()
    if len(data) == n and hashlib.sha256(data).hexdigest()[:16] == h:
        ok += 1
    else:
        bad += 1; print("BAD", p, len(data), n)
unlisted = []
for d, _, fs in os.walk(root):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), root)
        if rel != "INDEX.md" and rel not in listed:
            unlisted.append(rel)
for u in unlisted:
    print("UNLISTED", u)
print(f"rows={rows} ok={ok} bad={bad} missing={missing} unlisted={len(unlisted)}")
sys.exit(0 if bad == 0 and missing == 0 else 1)
