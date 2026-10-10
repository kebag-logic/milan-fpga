#!/usr/bin/env python3
"""Compare two record_configs.py outputs: explorations, configurations (flags+label), and what each read.
Usage: python3 -I compare_configs.py a.json b.json"""
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
ra, rb = a["record"], b["record"]
print("explorations", len(ra), len(rb), "configurations", a["configurations"], b["configurations"])
print("exploration keys equal:", set(ra) == set(rb))
for k in sorted(set(ra) ^ set(rb)):
    print("  only in", "a" if k in ra else "b", k[:300])
cfg = lambda r: {(k, row[0], row[1]) for k, v in r.items() for rows in v for row in rows}
full = lambda r: {(k, json.dumps(row)) for k, v in r.items() for rows in v for row in rows}
ca, cb_ = cfg(ra), cfg(rb)
print("configuration (unit, flags, label) sets equal:", ca == cb_, len(ca), len(cb_))
fa, fb = full(ra), full(rb)
print("configuration + deps + tested + error sets equal:", fa == fb)
for x in sorted(fa ^ fb)[:10]:
    print("  differs", ("a" if x in fa else "b"), x[0][:120], x[1][:300])
print("findings", a["findings"], b["findings"])
sys.exit(0 if ca == cb_ and fa == fb and set(ra) == set(rb) else 1)
