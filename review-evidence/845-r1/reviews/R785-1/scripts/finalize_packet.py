#!/usr/bin/env python3
"""Normalise receipts' absolute paths and write MANIFEST.sha256.

Usage: finalize_packet.py <packet dir> <clone dir>

Paths under the packet and the clone become <packet> and <clone>, so a receipt
names no host path. Every file under receipts/ and scripts/ is then listed.
REPORT.md is published separately and is not listed.
"""
import hashlib
import pathlib
import sys

packet = pathlib.Path(sys.argv[1]).resolve()
clone = pathlib.Path(sys.argv[2]).resolve()
files = sorted(p for d in ("receipts", "scripts") for p in (packet / d).rglob("*") if p.is_file())
for path in files:
    if path.parent.name != "receipts":
        continue
    data = path.read_bytes()
    data = data.replace(str(packet).encode(), b"<packet>").replace(str(clone).encode(), b"<clone>")
    data = data.replace(str(pathlib.Path.home()).encode(), b"<home>")
    path.write_bytes(data)
lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(packet)}\n" for p in files]
(packet / "MANIFEST.sha256").write_text("".join(lines))
print(f"{len(lines)} files listed")
