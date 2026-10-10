#!/usr/bin/env python3
"""List every -D/-U token in the boundary gate's builders that its flag reader neither reads as a mode or value
nor refuses. Usage: python3 -I scan_unread_flags.py <tree>"""
import re, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_configs as c  # noqa: E402
TOKEN = re.compile(r"(?<![\w-])-[DU]([A-Za-z_]\w*)")
unread = 0
for path, text in c.checkout_builders():
    flags, values = c.builder_flags(path, text)
    known = {c.FLAG.fullmatch(f)[1] for f in flags} | set(values)
    for n, line in enumerate(text.splitlines(), 1):
        for m in TOKEN.finditer(line):
            if m[1] not in known:
                unread += 1
                print(f"{c.rel(path)}:{n}: -{line[m.start()+1]}{m[1]} not read: {line.strip()[:140]}")
print(f"unread -D/-U tokens: {unread}")
