#!/usr/bin/env python3
"""List every kebag-logic/milan-fpga blob citation in a donor checkout's tracked
Markdown and print the cited parent lines.

usage: parent_citations.py DONOR_REPO PARENT_REPO [--changed BASE]
Exit 1 if any citation does not resolve (missing path, missing line).
"""
import re, subprocess, sys
from collections import OrderedDict

donor, parent = sys.argv[1], sys.argv[2]
base = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--changed" else None
RX = re.compile(r"https://github\.com/kebag-logic/milan-fpga/blob/([0-9a-f]{7,40})/([^\s)#]+)(?:#L(\d+)(?:-L(\d+))?)?")

def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)

files = git(donor, "ls-files", "*.md").stdout.split()
if base:
    files = git(donor, "diff", "--name-only", base, "HEAD", "--", "*.md").stdout.split()
occ, targets, bad = [], OrderedDict(), 0
for f in files:
    for n, line in enumerate(open(f"{donor}/{f}", encoding="utf-8"), 1):
        for m in RX.finditer(line):
            occ.append((f, n, m.groups()))
            targets.setdefault(m.groups(), []).append(f"{f}:{n}")
print(f"occurrences {len(occ)} targets {len(targets)}")
for (sha, path, a, b), where in targets.items():
    r = git(parent, "show", f"{sha}:{path}")
    print(f"\n== {sha[:8]} {path} L{a}{'-L'+b if b else ''}  cited x{len(where)} at {', '.join(where)}")
    if r.returncode:
        print("   UNRESOLVED path"); bad += 1; continue
    lines = r.stdout.splitlines()
    if a:
        lo, hi = int(a), int(b or a)
        if hi > len(lines) or lo > hi:
            print(f"   UNRESOLVED line (file has {len(lines)})"); bad += 1; continue
        for k in range(lo, hi + 1):
            print(f"   {k:5d}| {lines[k-1]}")
print(f"\nunresolved {bad}")
sys.exit(1 if bad else 0)
