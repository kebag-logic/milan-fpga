#!/usr/bin/env python3
"""Verify an author packet: MANIFEST.json published_sha256 for author-r29 files and receipts/INDEX.md rows.
Usage: verify_packet.py <665s2b-r1 dir> <subdir name, e.g. author-r29>"""
import hashlib, json, re, sys
from pathlib import Path
root, sub = Path(sys.argv[1]), sys.argv[2]
pk = root / sub
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
m = json.loads((root / "MANIFEST.json").read_text())
ent = [e for e in m if e["file"].startswith(sub + "/")]
bad = [e["file"] for e in ent if not (root / e["file"]).is_file() or h(root / e["file"]) != e["published_sha256"]]
files = {str(p.relative_to(root)) for p in pk.rglob("*") if p.is_file()}
unlisted = sorted(files - {e["file"] for e in ent})
print(f"manifest entries for {sub}: {len(ent)} bad {len(bad)} unlisted-in-manifest {len(unlisted)}")
for b in bad[:20]: print("  BAD", b)
for u in unlisted[:20]: print("  UNLISTED", u)
rows = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$", (pk / "receipts/INDEX.md").read_text(), re.M)
ib = [r[0] for r in rows if not (pk / r[0]).is_file() or h(pk / r[0]) != r[2] or (pk / r[0]).stat().st_size != int(r[1].replace(",", ""))]
listed = {r[0] for r in rows}
iu = sorted(f[len(sub)+1:] for f in files if f[len(sub)+1:] not in listed and f[len(sub)+1:] != "receipts/INDEX.md")
print(f"INDEX rows {len(rows)} bad {len(ib)} unlisted {len(iu)}")
for b in ib[:20]: print("  IBAD", b)
for u in iu[:20]: print("  IUNLISTED", u)
