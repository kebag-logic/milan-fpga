#!/usr/bin/env python3
"""Search a directory tree for a caller-supplied list of private tokens.

usage: scan_private_tokens.py <tokens-file> <dir> [<dir> ...]
The tokens file holds one "label<TAB>token" pair per line and is never published. Matching is
case-insensitive; alphanumeric tokens match on word boundaries so a short
account name does not match inside a longer word. Output prints only the label, never the token or its length, with counts and the first locations.
Exit 1 when any token is found, 0 otherwise. Binary files are scanned too.
"""
import re
import sys
from pathlib import Path

pairs = [x.split("\t", 1) for x in Path(sys.argv[1]).read_text().splitlines() if x.strip()]
labels = [p[0] for p in pairs]
toks = [p[1] for p in pairs]
pats = []
for t in toks:
    body = re.escape(t)
    if re.fullmatch(r"\w+", t):
        body = r"(?<![A-Za-z0-9])" + body + r"(?![A-Za-z0-9])"
    pats.append((t, re.compile(body.encode(), re.I)))
hits = {}
nfiles = 0
for d in sys.argv[2:]:
    root = Path(d)
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        nfiles += 1
        data = p.read_bytes()
        for t, pat in pats:
            for m in pat.finditer(data):
                line = data.count(b"\n", 0, m.start()) + 1
                hits.setdefault(t, []).append(f"{p.relative_to(root)}:{line}")
print(f"files scanned: {nfiles}; tokens: {len(toks)}")
for i, t in enumerate(toks):
    where = hits.get(t, [])
    print(f"  token {i:02d} [{labels[i]}]: {len(where)} hits" + (f" at {', '.join(where[:4])}" if where else ""))
print(f"TOTAL HITS: {sum(len(v) for v in hits.values())}")
sys.exit(1 if hits else 0)
