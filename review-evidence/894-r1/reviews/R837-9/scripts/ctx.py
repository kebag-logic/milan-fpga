#!/usr/bin/env python3
"""ctx.py <repo> <hits> [linefilter-regex]: print each hit token with 160
chars of context on its line."""
import sys, re, pathlib
repo = pathlib.Path(sys.argv[1]); flt = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
for h in open(sys.argv[2]):
    p, n, t = h.rstrip("\n").split(":")
    if flt and not flt.search(p + ":" + n):
        continue
    line = (repo / p).read_text(errors="replace").splitlines()[int(n) - 1]
    for m in re.finditer(r"(?<![\d.])" + re.escape(t) + r"(?![\d])", line):
        print(f"{p}:{n}:{t}: ...{line[max(0,m.start()-160):m.end()+80]}...")
