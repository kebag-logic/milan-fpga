#!/usr/bin/env python3
"""R624-9: compare two probe-rerun JSON files on their readings only (every integer, boolean and short
upper-case verdict string, by path), ignoring notes, commits and quoted page text.
usage: compare_probe_readings.py <round 8 dir> <round 9 dir> <out.json>"""
import json
import re
import sys
from pathlib import Path


def leaves(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, f"{path}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f"{path}[{i}]")
    elif isinstance(x, (bool, int)) or (isinstance(x, str) and re.fullmatch(r"[A-Z_]{2,12}", x)):
        yield path, x


a, b = Path(sys.argv[1]), Path(sys.argv[2])
out = {}
for f in sorted(a.glob("*-probe-rerun.json")):
    A, B = dict(leaves(json.load(open(f)))), dict(leaves(json.load(open(b / f.name))))
    diffs = {k: [A.get(k), B.get(k)] for k in sorted(set(A) | set(B)) if A.get(k) != B.get(k)}
    out[f.name] = dict(readings=len(A), differing=diffs)
    print(f.name, len(A), "readings,", len(diffs), "differ", list(diffs.items())[:3])
json.dump(out, open(sys.argv[3], "w"), indent=1)
