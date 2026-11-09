#!/usr/bin/env python3
"""Compare tb/srp_encoder/README.md arm rows of the form | `arm`: ... | row | N FAIL ... |
with the campaign's srp_encoder line for that arm (the first line whose tags carry no AP/OV/M/K row).
Usage: cmp_enc_readme.py <repo> <campaign.log>"""
import re, sys, pathlib
repo, log = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).read_text().splitlines()
rows = {}
for l in (repo / "tb/srp_encoder/README.md").read_text().splitlines():
    m = re.match(r"^\| `([a-z0-9-]+)`:[^|]*\|[^|]*\| (\d+) FAIL", l)
    if m: rows.setdefault(m.group(1), int(m.group(2)))
camp = {}
for l in log:
    m = re.match(r"^([a-z0-9-]+): rc=\d+ failures=(\d+) KILLED tags=(.*)$", l)
    if not m: continue
    tags = m.group(3).split(",")
    if any(re.match(r"^(AP|OV|M|K|L|N|O|P|Q|R|S|SW|DJ)\d+$", t) for t in tags): continue
    camp.setdefault(m.group(1), int(m.group(2)))
bad = 0
for a, n in rows.items():
    c = camp.get(a)
    if c != n: print(f"DIFF {a}: README {n}, campaign {c}"); bad += 1
print(f"{len(rows)} encoder README rows compared, {bad} differ")
