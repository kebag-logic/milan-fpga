#!/usr/bin/env python3
"""Check RECEIPTS.md against the directory: the same set of files, each with
the recorded size and sha256. Usage: verify_receipts.py <outdir>"""
import hashlib, re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
rows = {}
for line in (root / "RECEIPTS.md").read_text().splitlines():
    m = re.match(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|", line)
    if m and not m.group(1).startswith("/"):
        rows[m.group(1)] = (int(m.group(2)), m.group(3))
files = {p.relative_to(root).as_posix(): p for p in root.rglob("*")
         if p.is_file() and p.name != "RECEIPTS.md"}
bad = sorted(set(rows) ^ set(files))
for rel in sorted(set(rows) & set(files)):
    data = files[rel].read_bytes()
    if (len(data), hashlib.sha256(data).hexdigest()) != rows[rel]:
        bad.append(rel)
print(f"{len(files)} files, {len(rows)} index rows, {len(bad)} mismatches")
for b in bad:
    print("MISMATCH", b)
sys.exit(1 if bad else 0)
