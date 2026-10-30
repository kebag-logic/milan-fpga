#!/usr/bin/env python3
"""Verify a review-evidence tree against its MANIFEST.json and an author INDEX.md.
usage: verify_packet.py <evidence-root (review-evidence/806-r1)> <subdir with INDEX.md>"""
import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1]); sub = root / sys.argv[2]
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
man = json.loads((root / "MANIFEST.json").read_text())
bad = 0; listed = set()
for e in man:
    p = root / e["file"]; listed.add(e["file"])
    if not p.is_file() or h(p) != e["published_sha256"]:
        bad += 1; print("MANIFEST MISMATCH", e["file"])
present = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
unl = sorted(present - listed)
print("manifest entries", len(man), "mismatches", bad, "unlisted files", len(unl), unl[:10])
ib = 0; n = 0
for line in (sub / "INDEX.md").read_text().splitlines():
    m = re.match(r"\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|", line)
    if not m: continue
    n += 1; p = sub / m[1]
    if not p.is_file() or h(p) != m[3] or p.stat().st_size != int(m[2].replace(",", "")):
        ib += 1; print("INDEX MISMATCH", m[1])
print("index entries", n, "mismatches", ib)
sys.exit(1 if bad or ib or unl else 0)
