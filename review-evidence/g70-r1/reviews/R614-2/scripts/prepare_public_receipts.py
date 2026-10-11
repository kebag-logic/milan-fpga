#!/usr/bin/env python3
"""Path/host-only redaction of publishable receipts; retain raw originals in scratch.

Usage: prepare_public_receipts.py PACKET REPO
Run once before generating MANIFEST.sha256. No numbers or findings are changed.
"""
import os
from pathlib import Path
import re
import shutil
import sys

packet, repo = map(lambda p: Path(p).resolve(), sys.argv[1:])
raw = packet / "scratch" / "raw_receipts"
raw.mkdir(parents=True, exist_ok=True)
for path in sorted((packet / "receipts").rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(packet / "receipts")
    backup = raw / rel
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    text = backup.read_text()
    for before, after in ((str(packet), "<review-packet>"), (str(repo), "<review-checkout>"), (str(Path.home()), "<home>"), ("$VALIDATION_TOOLS/pinned-verilator-5.050", "<pinned-simulator>")):
        text = text.replace(before, after)
    text = re.sub(r"(?m)^(\| Host\s*:).*$", r"\1 <host>", text)
    path.write_text(text)
print("PASS: publishable receipts redacted; raw originals retained under scratch/raw_receipts")
