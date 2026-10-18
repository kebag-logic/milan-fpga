#!/usr/bin/env python3
"""publish.py <dest> <src>=<rel> ...: copy each scratch file to <dest>/<rel>, with host
paths replaced by placeholders (<scratch>, <lane>, <tools>, <home>); refuses files over
200 KB after redaction."""
import sys
from pathlib import Path
SUBS = [("<scratch>", "<scratch>"), ("<lane>", "<lane>"),
        ("<tools>", "<tools>"), ("<home>", "<home>"), ("<data>", "<data>")]
dest = Path(sys.argv[1])
for arg in sys.argv[2:]:
    src, rel = arg.split("=", 1)
    data = Path(src).read_bytes()
    for a, b in SUBS:
        data = data.replace(a.encode(), b.encode())
    if len(data) > 200 * 1024:
        sys.exit(f"refused: {src} is {len(data)} bytes")
    out = dest / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
print(f"published {len(sys.argv) - 2} files")
