#!/usr/bin/env python3
"""Replace every receipt over 200 KB with an excerpt, recording the original's size and sha256.

usage: python3 -B trim_large.py OUTDIR

Each FILE over the limit becomes FILE.excerpt (its first 40 and last 120
lines) and is removed; receipts/LARGE-FILES.txt keeps one line per original:
size, sha256, path. Run before index_receipts.py.
"""
import hashlib
import sys
from pathlib import Path

out = Path(sys.argv[1]).resolve()
receipts = out / "receipts"
LIMIT = 200 * 1024
ledger = receipts / "LARGE-FILES.txt"
lines = ledger.read_text().splitlines() if ledger.exists() else [
    "# receipts over 200 KB, replaced by an excerpt (first 40 and last 120 lines): size sha256 path"]
for path in sorted(p for p in receipts.rglob("*") if p.is_file()):
    data = path.read_bytes()
    if len(data) <= LIMIT:
        continue
    rel = path.relative_to(receipts).as_posix()
    lines.append(f"{len(data)} {hashlib.sha256(data).hexdigest()} {rel}")
    text = data.decode(errors="replace").splitlines()
    excerpt = text[:40] + [f"... {len(text) - 160} lines omitted; see LARGE-FILES.txt ..."] + text[-120:]
    path.with_name(path.name + ".excerpt").write_text("\n".join(excerpt) + "\n")
    path.unlink()
    print(f"trimmed {rel} ({len(data)} B)")
ledger.write_text("\n".join(lines) + "\n")
