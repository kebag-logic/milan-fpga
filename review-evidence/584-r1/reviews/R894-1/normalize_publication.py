#!/usr/bin/env python3
"""Normalize installation paths, keeping original receipts under excluded scratch."""
from pathlib import Path
import re
import sys

packet = Path(__file__).resolve().parent
root = str(Path(sys.argv[1]).resolve())
compiler = str(Path(sys.argv[2]).resolve())
originals = packet / 'scratch/raw-receipts'
originals.mkdir(parents=True, exist_ok=True)
for path in sorted(packet.iterdir()):
    if not path.is_file() or path.suffix not in ('.log', '.txt', '.json'):
        continue
    data = path.read_bytes()
    backup = originals / path.name
    if not backup.exists(): backup.write_bytes(data)
    text = data.decode()
    text = text.replace(root, '<review-root>').replace(str(packet), '<packet>')
    text = text.replace(compiler, '<pinned-verilator>')
    text = re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff',
                  '<compiler-runtime>', text)
    path.write_text(text)
