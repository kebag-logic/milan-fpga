#!/usr/bin/env python3
"""Every tb/srp_top/README.md table row '| `arm`... | ... | N | ...' whose arm the campaign grades
on srp_top (a log line whose tags are srp_top rows): compare the first integer cell with the
campaign count. Usage: cmp_top_readme.py <repo> <campaign.log> [<base-repo-ref-README>]"""
import re, sys, pathlib
repo, log = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).read_text().splitlines()
TOP = re.compile(r"^(AP|OV|M|K|L|N|O|P|Q|R|S|SC|TF|WK|RB|DJ|SH|SW|TP|PS|LK)\d+$")
camp = {}
for l in log:
    m = re.match(r"^([a-z0-9-]+): rc=\d+ failures=(\d+) KILLED tags=(.*)$", l)
    if m and all(TOP.match(t) for t in m.group(3).split(",")):
        camp.setdefault(m.group(1), []).append(int(m.group(2)))
bad = n = 0
for i, l in enumerate((repo / "tb/srp_top/README.md").read_text().splitlines(), 1):
    m = re.match(r"^\| `([a-z0-9-]+)`[^|]*\|(.*)$", l)
    if not m or m.group(1) not in camp: continue
    cells = [c.strip() for c in m.group(2).split("|")]
    num = next((int(c) for c in cells if re.fullmatch(r"\d+", c)), None)
    if num is None: continue
    n += 1
    if num not in camp[m.group(1)]:
        bad += 1; print(f"DIFF README:{i} {m.group(1)}: README {num}, campaign {camp[m.group(1)]}")
print(f"{n} srp_top README rows compared, {bad} differ")
