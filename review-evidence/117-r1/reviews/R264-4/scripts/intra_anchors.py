#!/usr/bin/env python3
"""Resolve every same-page and cross-page fragment link in the given pages
against GitHub-style heading slugs. usage: intra_anchors.py <repo> <page>..."""
import os
import re
import sys


def slugs(path):
    out, seen = set(), {}
    fence = False
    for line in open(path, encoding="utf-8"):
        if line.startswith("```"):
            fence = not fence
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        t = re.sub(r"`", "", m.group(2)).strip().lower()
        t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
        n = seen.get(t, 0)
        seen[t] = n + 1
        out.add(t if n == 0 else f"{t}-{n}")
    return out


repo = sys.argv[1]
bad = 0
for page in sys.argv[2:]:
    p = os.path.join(repo, page)
    text = open(p, encoding="utf-8").read()
    links = re.findall(r"\]\(([^)\s]*)#([^)\s]+)\)", text)
    for target, frag in links:
        if target.startswith("http"):
            continue
        tp = os.path.normpath(os.path.join(os.path.dirname(p), target)) if target else p
        ok = frag in slugs(tp)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {page} -> {target or '(same page)'}#{frag}")
print("RESULT", "PASS" if bad == 0 else f"FAIL {bad}")
