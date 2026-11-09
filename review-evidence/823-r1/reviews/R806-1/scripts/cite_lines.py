#!/usr/bin/env python3
"""cite_lines.py ROOT PAGE: print every `path:line` the page cites with the cited line's text."""
import re, sys
from pathlib import Path
root, page = Path(sys.argv[1]), Path(sys.argv[2])
for n, line in enumerate(page.read_text().splitlines(), 1):
    for m in re.finditer(r"`([\w./-]+\.\w+):(\d+)`", line):
        p, ln = root / m.group(1), int(m.group(2))
        text = p.read_text(errors="replace").splitlines()[ln - 1].strip() if p.exists() else "<NO FILE>"
        print(f"page:{n} -> {m.group(1)}:{ln}: {text[:110]}")
