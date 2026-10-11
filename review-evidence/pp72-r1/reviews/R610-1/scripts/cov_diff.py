#!/usr/bin/env python3
"""Compare every REQ row of 00 section 6 at two revisions, cell by cell.
usage: cov_diff.py REPO BASE HEAD"""
import re, subprocess, sys
repo, base, head = sys.argv[1:4]
ROW = re.compile(r"^\|\s*(REQ-[A-Z]+-\d{3})\s*\|(.*)$", re.M)
def rows(rev):
    t = subprocess.run(["git", "-C", repo, "show", f"{rev}:docs/00_MILAN_COMPLIANCE_REVIEW.md"],
                       capture_output=True, text=True, check=True).stdout
    return {r: [c.strip() for c in rest.split("|")] for r, rest in ROW.findall(t)}
b, h = rows(base), rows(head)
print(f"rows base {len(b)} head {len(h)}; only base {sorted(set(b)-set(h))}; only head {sorted(set(h)-set(b))}")
names = ["Clause", "Requirement", "Mand", "Cov", "Finding", "Arch", "Doc", "Ver"]
for r in b:
    if r not in h: continue
    for i, n in enumerate(names):
        bv, hv = b[r][i], h[r][i]
        if bv == hv: continue
        if n == "Cov" and hv.startswith(bv[:1]) and (hv == bv or hv.split("; ", 1)[0] == bv):
            continue  # suffix only
        print(f"{r} {n}: BASE '{bv[:300]}' HEAD '{hv[:300]}'")
