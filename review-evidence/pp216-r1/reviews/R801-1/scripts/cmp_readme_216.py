#!/usr/bin/env python3
"""Compare the issue #216 arm rows of tb/srp_top/README.md (srp_top group 'applicant' table:
| `arm` (...) | N | rows |) with the campaign log's srp_top applicant failure counts.
Usage: cmp_readme_216.py <repo> <campaign.log>"""
import re, sys, pathlib
repo, log = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).read_text().splitlines()
txt = (repo / "tb/srp_top/README.md").read_text().splitlines()
start = next(i for i, l in enumerate(txt) if re.match(r"^#+ .*#216", l))
rows = {}
for l in txt[start:]:
    m = re.match(r"^\| `([a-z0-9-]+)`[^|]*\| (\d+) \| (AP[^|]*)\|", l)
    if m: rows.setdefault(m.group(1), int(m.group(2)))
camp = {}
for l in log:
    m = re.match(r"^([a-z0-9-]+): rc=\d+ failures=(\d+) KILLED tags=(.*)$", l)
    if m and re.search(r"\bAP\d", m.group(3)):
        camp.setdefault(m.group(1), int(m.group(2)))
bad = 0
for a, n in rows.items():
    c = camp.get(a)
    print(f"{a}: README {n}, campaign {c} {'OK' if c == n else 'DIFF'}")
    bad += c != n
print(f"{len(rows)} rows, {bad} differ")
sys.exit(1 if bad else 0)
