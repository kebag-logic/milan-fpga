#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R458-2: the PR body's round-1 control table (2/2, 9/9, 3/5, 1/1 columns) and
HANDOFF 4.2's, cell by cell, against the published controls-final.log; and the
'Caught at' column against the count of non-zero cells.
usage: check_r1_table.py <controls-final.log> <markdown file> [...]"""
import re, sys
log = {}
for ln in open(sys.argv[1]):
    m = re.match(r"(\S+) n(\d+) .*mismatch_cycles\(top\+internal\)=(\d+)", ln)
    if m:
        log[(m.group(1), {"2": "2/2", "9": "9/9", "35": "3/5", "1": "1/1"}[m.group(2)])] = int(m.group(3))
for md in sys.argv[2:]:
    bad = rows = 0
    for ln in open(md):
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) != 7 or not c[0].startswith("`") or not re.match(r"\d of 4", c[6]):
            continue
        name = c[0].strip("`")
        if (name, "2/2") not in log:
            continue
        rows += 1
        cells = dict(zip(["2/2", "9/9", "3/5", "1/1"], c[2:6]))
        nz = 0
        for sh, v in cells.items():
            n = int(re.match(r"([\d,]+)", v).group(1).replace(",", ""))
            nz += n != 0
            if n != log[(name, sh)]:
                bad += 1; print(f"{md}: {name} {sh}: table {n} log {log[(name, sh)]}")
        if f"{nz} of 4" != c[6]:
            bad += 1; print(f"{md}: {name}: caught-at {c[6]} but {nz} non-zero cells")
    print(f"{md}: {rows} rows, {bad} mismatches")
