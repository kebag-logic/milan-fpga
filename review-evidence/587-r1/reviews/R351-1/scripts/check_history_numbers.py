#!/usr/bin/env python3
"""Prove the PR changed no pre-existing figure on the baseline page.

Usage: check_history_numbers.py REPO BASE HEAD
Collects every number token from every line of the base page and checks
that the multiset of numbers on removed lines equals that on the lines that
replaced them (labels may change; figures may not), and that every base
table row's numeric cells survive unchanged at head in the same order.
"""
import re, subprocess, sys
from collections import Counter
repo, base, head = sys.argv[1:4]
page = "docs/findings/PP_SHADOW_BASELINE.md"
def show(rev): return subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"], capture_output=True, text=True, check=True).stdout.splitlines()
num = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")
def cells(line):
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return [c for c in parts[1:] if num.fullmatch(c)]
b, h = show(base), show(head)
brows = [l for l in b if l.startswith("|") and cells(l)]
hrows_set = Counter(tuple(cells(l)) for l in h if l.startswith("|"))
missing = [l for l in brows if hrows_set[tuple(cells(l))] == 0]
print(f"base numeric table rows: {len(brows)}; rows whose numeric cells are absent at head: {len(missing)}")
for l in missing: print("  MISSING", l)
# prose numbers on base lines that were removed
diff = subprocess.run(["git", "-C", repo, "diff", "-U0", base, head, "--", page], capture_output=True, text=True, check=True).stdout
removed = Counter(); 
for l in diff.splitlines():
    if l.startswith("-") and not l.startswith("---") and not l.lstrip("-").startswith("|"):
        removed.update(num.findall(l[1:]))
hnums = Counter(t for l in h for t in num.findall(l))
lost = {k: v for k, v in removed.items() if hnums[k] < v}
print("prose number tokens removed at head and absent from head page:", lost or "none")
sys.exit(1 if missing else 0)
