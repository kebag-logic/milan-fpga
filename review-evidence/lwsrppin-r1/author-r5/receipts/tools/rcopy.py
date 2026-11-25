#!/usr/bin/env python3
"""rcopy.py SRC DST [EXTRACT]: copy a text log into the receipts, under 200 KB.

A log over 190,000 bytes is kept as its first and last 90,000 bytes, with its full size and sha256 noted where the
middle is cut. With EXTRACT, DST.results.txt also gets every line that starts with '[' or names a verdict, a PASS,
a mutant tally or the gate's result, from the full log (itself kept under 190,000 bytes the same way).
"""
import hashlib
import re
import sys
from pathlib import Path

LIMIT, KEEP = 190_000, 90_000


def fit(data: bytes, name: str) -> bytes:
    """The data, or its head and tail with a note, so that it stays under LIMIT."""
    if len(data) <= LIMIT:
        return data
    note = (f"\n\n[... {name}: {len(data):,} bytes in full, sha256 {hashlib.sha256(data).hexdigest()}; "
            f"the middle {len(data) - 2 * KEEP:,} bytes are cut here, the first and last {KEEP:,} kept ...]\n\n")
    return data[:KEEP] + note.encode() + data[-KEEP:]


src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.parent.mkdir(parents=True, exist_ok=True)
raw = src.read_bytes()
dst.write_bytes(fit(raw, src.name))
if len(sys.argv) > 3:
    pat = re.compile(r"^\[|verdict:|PASS|mutants:|caught|test_ctrl_firmware:|exactly one shard")
    lines = [l for l in raw.decode(errors="replace").splitlines() if pat.search(l)]
    out = Path(str(dst) + ".results.txt")
    out.write_bytes(fit(("\n".join(lines) + "\n").encode(), out.name))
