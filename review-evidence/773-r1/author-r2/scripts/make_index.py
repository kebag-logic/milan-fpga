#!/usr/bin/env python3
"""Generate receipts/INDEX.md from the files present (size and sha256)."""
import hashlib, os, sys
root = sys.argv[1]
rows = []
for d, _, fs in os.walk(root):
    for f in sorted(fs):
        if f == "INDEX.md":
            continue
        p = os.path.join(d, f)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        rows.append((os.path.relpath(p, root), os.path.getsize(p), h))
rows.sort()
with open(os.path.join(root, "INDEX.md"), "w") as o:
    o.write("# Receipts index (generated from the files present by scripts/make_index.py)\n\n")
    o.write("| File | Bytes | sha256 |\n|---|---:|---|\n")
    for r, s, h in rows:
        o.write(f"| `{r}` | {s:,} | `{h}` |\n")
print(len(rows), "files")
