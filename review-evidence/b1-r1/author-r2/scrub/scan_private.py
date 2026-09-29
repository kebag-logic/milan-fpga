#!/usr/bin/env python3
"""Scan a directory for the lane's private tokens and print masked counts only.

usage: scan_private.py <dir> <private-token-file>

The token file is private and stays outside the packet: a JSON list of
{"kind": ..., "token": ...} holding the bench host names, the console port,
interface names, the local account name, the capture host's NIC MACs, the
controller host's NIC MAC and its MAC-derived EUI-64, and the tap driver
name. Matching is case-insensitive and byte-wise over every file, binary or
text. Only the kind and the count are printed, never a token. Exit 1 on any
hit.
"""
import collections
import json
import sys
from pathlib import Path

root, tokfile = Path(sys.argv[1]), Path(sys.argv[2])
toks = json.loads(tokfile.read_text())
hits = collections.Counter()
where = collections.defaultdict(set)
n = 0
for p in sorted(root.rglob("*")):
    if not p.is_file():
        continue
    n += 1
    b = p.read_bytes().lower()
    for t in toks:
        c = b.count(t["token"].lower().encode())
        if c:
            hits[t["kind"]] += c
            where[t["kind"]].add(p.relative_to(root).as_posix())
print(f"private-token scan: {n} files, {len(toks)} tokens in {len({t['kind'] for t in toks})} kinds")
for k in sorted({t["kind"] for t in toks}):
    print(f"  {k}: {hits[k]} hits{' in ' + ', '.join(sorted(where[k])) if hits[k] else ''}")
print(f"TOTAL {sum(hits.values())}")
sys.exit(1 if hits else 0)
