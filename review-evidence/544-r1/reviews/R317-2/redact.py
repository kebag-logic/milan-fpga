#!/usr/bin/env python3
"""Replace the reviewer host's home prefix with $HOME in every receipt (R317-1)."""
import os, pathlib, sys
home = os.path.expanduser("~"); total = 0; log = []
for p in sorted(pathlib.Path("receipts").rglob("*")):
    if p.is_file():
        t = p.read_bytes(); n = t.count(home.encode())
        if n:
            p.write_bytes(t.replace(home.encode(), b"$HOME")); total += n; log.append(f"{p}: {n}")
pathlib.Path("receipts/redaction.txt").write_text(
    "home prefix replaced by $HOME; nothing else changed\n" + "\n".join(log) + f"\ntotal {total}\n")
print(total)
