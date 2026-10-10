#!/usr/bin/env python3
"""Check every in-page '#fragment' link of a Markdown page resolves to a
GitHub-style heading slug on the same page (fenced code excluded)."""
import re, sys
from collections import Counter
path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")
slugs, seen, fence = set(), Counter(), False
for ln in lines:
    if ln.lstrip().startswith("```"):
        fence = not fence; continue
    if fence: continue
    m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", ln)
    if not m: continue
    t = re.sub(r"`", "", m.group(2)).lower()
    t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
    s = t if seen[t] == 0 else f"{t}-{seen[t]}"
    seen[t] += 1; slugs.add(s)
bad = 0; n = 0
for i, ln in enumerate(lines, 1):
    for frag in re.findall(r"\]\(#([^)]+)\)", ln):
        n += 1
        if frag not in slugs:
            bad += 1; print(f"UNRESOLVED {path}:{i} #{frag}")
print(f"in-page links {n}, unresolved {bad}")
sys.exit(1 if bad else 0)
