#!/usr/bin/env python3
"""Scan files for private names and forbidden tokens, printing labels only (read-only).

usage: token_scan.py <redact-map.json> <regex-tokens.txt> <literal-names.txt> <path>...

The token sources stay outside this packet:
  redact-map.json    the lane's private redaction map: {"literal": [[value, label]...],
                     "regex": [[pattern, label]...]};
  regex-tokens.txt   one case-insensitive regex per line ('#' lines are comments);
  literal-names.txt  one case-insensitive literal per line.
A hit is reported as file:line and the token's label or source line number, never the
matched text. Exit 1 on any hit.
"""
import json
import re
import sys
from pathlib import Path

rmap, regf, litf, *paths = sys.argv[1:]
m = json.load(open(rmap))
toks = [(re.compile(re.escape(v), re.I), f"map {lab}") for v, lab in m.get("literal", []) if v]
toks += [(re.compile(p, re.I), f"map {lab}") for p, lab in m.get("regex", [])]
for i, line in enumerate(open(regf), 1):
    line = line.rstrip("\n")
    if line and not line.startswith("#"):
        toks.append((re.compile(line, re.I), f"regex list line {i}"))
for i, line in enumerate(open(litf), 1):
    line = line.strip()
    if line:
        toks.append((re.compile(re.escape(line), re.I), f"name list line {i}"))

files = []
for p in paths:
    p = Path(p)
    files += sorted(x for x in p.rglob("*") if x.is_file()) if p.is_dir() else [p]
hits = 0
for f in files:
    try:
        text = f.read_text(errors="replace")
    except OSError:
        continue
    for n, line in enumerate(text.split("\n"), 1):
        for rx, lab in toks:
            if rx.search(line):
                hits += 1
                print(f"HIT {f.name}:{n}: {lab}")
print(f"scanned {len(files)} file(s) against {len(toks)} token(s): {hits} hit(s)")
sys.exit(1 if hits else 0)
