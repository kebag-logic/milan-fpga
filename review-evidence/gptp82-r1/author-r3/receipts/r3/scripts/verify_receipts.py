#!/usr/bin/env python3
"""Check RECEIPTS.md against the directory. Only the table under the
"## In this directory" heading is read, up to the next "## " heading, so
the separately declared scratch table never enters the comparison, however
its paths are spelled. Usage: verify_receipts.py <outdir>"""
import hashlib, re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
rows, inside, seen = {}, False, False
for line in (root / "RECEIPTS.md").read_text().splitlines():
    if line.startswith("## "):
        inside = line.strip() == "## In this directory"
        seen |= inside
        continue
    m = re.match(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|", line)
    if inside and m:
        if m.group(1) in rows:
            print("DUPLICATE ROW", m.group(1)); sys.exit(1)
        rows[m.group(1)] = (int(m.group(2)), m.group(3))
if not seen:
    print("no '## In this directory' table"); sys.exit(1)
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
