#!/usr/bin/env python3
"""Resolve every fragment link in lines [a, b] of a page against GitHub-style heading slugs.
Usage: anchors.py <page> <first-line> <last-line>"""
import os, re, sys
page, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
def slugs(path):
    out, inf = set(), False
    for ln in open(path):
        if ln.startswith("```"):
            inf = not inf
        m = None if inf else re.match(r"#{1,6} (.*)", ln)
        if m:
            t = m.group(1).strip().lower()
            t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
            base, n = t, 1
            while t in out:
                t = f"{base}-{n}"; n += 1
            out.add(t)
    return out
lines = open(page).read().split("\n")[a - 1:b]
bad = 0
for i, ln in enumerate(lines, a):
    for tgt in re.findall(r"\]\(([^)]*#[^)]+)\)", ln):
        f, frag = tgt.split("#", 1)
        if f.startswith("http"):
            continue
        p = os.path.normpath(os.path.join(os.path.dirname(page), f)) if f else page
        ok = frag in slugs(p)
        bad += not ok
        print(("OK  " if ok else "BAD ") + f"{i}: {tgt}")
print("unresolved", bad)
