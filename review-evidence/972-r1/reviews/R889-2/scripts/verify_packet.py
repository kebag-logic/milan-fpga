#!/usr/bin/env python3
"""Check the author-r3 packet's files against review-evidence/972-r1/MANIFEST.json and receipts/INDEX.md.
usage: python3 -I verify_packet.py <review-evidence/972-r1 directory>"""
import hashlib, json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
ok = bad = 0
for e in json.loads((root / "MANIFEST.json").read_text()):
    if not e["file"].startswith("author-r3"):
        continue
    d = hashlib.sha256((root / e["file"]).read_bytes()).hexdigest()
    if d == e["published_sha256"]:
        ok += 1
    else:
        bad += 1
        print("MANIFEST MISMATCH", e["file"])
    if e.get("path_redacted"):
        print("REDACTED", e["file"], "original", e["original_sha256"], "published", e["published_sha256"])
print(f"MANIFEST author-r3: {ok} match, {bad} mismatch")
iok = ibad = 0
for line in (root / "author-r3/receipts/INDEX.md").read_text().splitlines():
    m = re.match(r"\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})`", line)
    if not m:
        continue
    d = hashlib.sha256((root / "author-r3/receipts" / m.group(1)).read_bytes()).hexdigest()
    if d == m.group(3):
        iok += 1
    else:
        ibad += 1
        print("INDEX MISMATCH", m.group(1))
print(f"INDEX: {iok} match, {ibad} mismatch")
