#!/usr/bin/env python3
"""Check the archived grade tool's channel-identification step for capture-layout
literals, without printing them. Reports line numbers and match counts only.
Usage: mask_check.py <git dir holding the evidence branch> <commit> [<commit> ...]"""
import re, subprocess, sys
repo, commits = sys.argv[1], sys.argv[2:]
P = "review-evidence/b6-r1/author/tools/grade_b6.py"
IDX = re.compile(r"w\[:, *\d+\]")              # a numeric column index into the capture
KEY = re.compile(r"pair_\d+_\d+")              # a result key that spells two indices
CNT = re.compile(r"words24\(full, *\d+\)|range\(\d+\)")  # a numeric channel count
bad = 0
for c in commits:
    src = subprocess.run(["git", "-C", repo, "show", f"{c}:{P}"], capture_output=True, text=True, check=True).stdout
    allines = src.splitlines()
    a = next(i for i, l in enumerate(allines) if l.startswith("# 1. channel identification"))
    z = next(i for i, l in enumerate(allines) if l.startswith("# 2."))
    for name, rx in (("numeric column index", IDX), ("index-spelling result key", KEY), ("numeric channel count", CNT)):
        # only the channel-identification block (code) and the module docstring's step 1
        lines = [i + 1 for i, l in enumerate(allines) if (a <= i < z or i < 12) and rx.search(l)]
        bad += bool(lines)
        print(f"{c[:8]} {P}: {name}: {len(lines)} line(s) {lines}")
    diff = subprocess.run(["git", "-C", repo, "show", "--format=", c, "--", P], capture_output=True, text=True).stdout
    removed = [l for l in diff.splitlines() if l.startswith("-") and not l.startswith("---") and (CNT.search(l) or IDX.search(l))]
    print(f"{c[:8]} own diff: removed lines carrying a numeric layout literal: {len(removed)}")
print("RESULT", "LAYOUT LITERALS PRESENT" if bad else "CLEAN")
