#!/usr/bin/env python3
"""Check the page's evidence-file table (bytes, SHA-256) against a packet tree.

usage: page_hashes.py <page.md> <packet author dir>
"""
import hashlib, os, re, sys
page, root = sys.argv[1], sys.argv[2]
rows = re.findall(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", open(page).read(), re.M)
bad = 0
for path, size, sha in rows:
    p = os.path.join(root, path)
    if not os.path.exists(p):
        print("ABSENT", path); continue
    b = open(p, "rb").read()
    ok = len(b) == int(size.replace(",", "")) and hashlib.sha256(b).hexdigest() == sha
    bad += not ok
    print("EQUAL " if ok else "DIFFER", path, len(b), hashlib.sha256(b).hexdigest()[:16])
print(f"rows {len(rows)} differ {bad}")
