#!/usr/bin/env python3
"""Copy receipts into receipts/published with host paths neutralised.
Usage: sanitize.py PACKET CLONE TOOLDIR FILE...   (FILE relative to PACKET)
"""
import sys
from pathlib import Path

packet, clone, tooldir = (Path(a).resolve() for a in sys.argv[1:4])
subs = [(str(packet), "<packet>"), (str(clone), "<clone>"), (str(tooldir), "<pinned-verilator>"),
        (str(Path.home()), "<home>")]
out = packet / "receipts" / "published"
out.mkdir(parents=True, exist_ok=True)
for rel in sys.argv[4:]:
    src = packet / rel
    text = src.read_text(errors="replace")
    for old, new in subs:
        text = text.replace(old, new)
    dst = out / src.name
    dst.write_text(text)
    print(dst.relative_to(packet))
