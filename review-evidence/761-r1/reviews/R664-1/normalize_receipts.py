#!/usr/bin/env python3
"""Retain original console bytes privately and normalize host paths for publication."""
from pathlib import Path
import hashlib
import os
import re

p = Path(__file__).resolve().parent
raw = p / "scratch/raw-receipts"
raw.mkdir(exist_ok=True)
rows = []
for f in sorted(p.glob("*.log")):
    original = f.read_bytes()
    (raw / f.name).write_bytes(original)
    text = original.decode()
    text = text.replace(str(p), "<packet>")
    text = text.replace(str(Path.home()), "$HOME")
    text = re.sub(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff", "<tools>", text)
    text = re.sub(r"\$HOME/\.local/share/containers/storage/overlay/[0-9a-f]+/diff", "<tools>", text)
    published = text.encode()
    f.write_bytes(published)
    rows.append(f"{f.name}\t{hashlib.sha256(original).hexdigest()}\t{hashlib.sha256(published).hexdigest()}\t{original != published}")
(p / "receipt-normalization.tsv").write_text("file\toriginal_sha256\tpublished_sha256\tpath_normalized\n" + "\n".join(rows) + "\n")
