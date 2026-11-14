#!/usr/bin/env python3
"""Verify every receipts/harness/scratch/ row of an author receipts/INDEX.md
against the published file bytes (size and sha256).

usage: verify_scratch_receipts.py <author-r3 dir>
exit 0 iff every listed row exists with matching size and sha256 and no
unlisted file is present under receipts/harness/scratch/.
"""
import hashlib, os, re, sys

root = sys.argv[1]
index = os.path.join(root, "receipts", "INDEX.md")
row = re.compile(r"^\| `(receipts/harness/scratch/[^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|")
listed = {}
with open(index, encoding="utf-8") as f:
    for line in f:
        m = row.match(line)
        if m:
            listed[m.group(1)] = (int(m.group(2)), m.group(3))
bad = 0
for rel, (size, digest) in sorted(listed.items()):
    p = os.path.join(root, rel)
    if not os.path.isfile(p):
        print(f"MISSING {rel}"); bad += 1; continue
    b = open(p, "rb").read()
    got = hashlib.sha256(b).hexdigest()
    ok = got == digest and len(b) == size
    print(f"{'OK  ' if ok else 'BAD '} {rel} size={len(b)}/{size} sha256={got}")
    bad += not ok
sd = os.path.join(root, "receipts", "harness", "scratch")
present = {f"receipts/harness/scratch/{n}" for n in os.listdir(sd)} if os.path.isdir(sd) else set()
for extra in sorted(present - set(listed)):
    print(f"UNLISTED {extra}"); bad += 1
print(f"listed={len(listed)} present={len(present)} bad={bad}")
sys.exit(1 if bad else 0)
