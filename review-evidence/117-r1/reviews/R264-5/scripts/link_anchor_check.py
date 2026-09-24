#!/usr/bin/env python3
"""Relative links and #fragments of the three changed pages resolve at the checkout.

Usage: link_anchor_check.py <checkout>
"""
import os
import re
import sys

os.chdir(sys.argv[1])


def slug(h):
    h = re.sub(r"[`*_]", "", h.strip().lower())
    return re.sub(r"[^\w\- ]", "", h).replace(" ", "-")


def anchors(p):
    a, seen, fence = set(), {}, False
    for line in open(p):
        if line.startswith("```"):
            fence = not fence
        if fence:
            continue
        m = re.match(r"#{1,6} (.*)", line)
        if m:
            s = slug(m.group(1))
            n = seen.get(s, 0)
            seen[s] = n + 1
            a.add(s if n == 0 else f"{s}-{n}")
    return a


bad = n = 0
pages = ["docs/findings/117_GPTP_SILICON_EVIDENCE.md", "docs/design/GM_LOSS_RECOVERY.md", "docs/findings/README.md"]
for f in pages:
    for m in re.finditer(r"\]\(([^)\s]+)\)", open(f).read()):
        t = m.group(1)
        if t.startswith("http"):
            continue
        n += 1
        path, _, frag = t.partition("#")
        tgt = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
        ok = os.path.exists(tgt) and (not frag or not tgt.endswith(".md") or frag in anchors(tgt))
        if not ok:
            bad += 1
            print("BROKEN", f, t)
print(f"relative links checked: {n}, broken: {bad}")
ext = set()
for f in pages:
    ext |= set(re.findall(r"https://github\.com/[^)\s]+", open(f).read()))
for e in sorted(ext):
    print("external", e)
