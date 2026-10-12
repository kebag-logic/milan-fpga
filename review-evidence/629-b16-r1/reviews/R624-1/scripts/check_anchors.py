#!/usr/bin/env python3
"""Check that every same-page and design-page fragment link added in a range resolves to a heading slug.

usage: check_anchors.py <repo> <base> <page.md>
"""
import re, subprocess, sys, os

repo, base, page = sys.argv[1:4]


def slugs(path):
    out = set()
    infence = False
    for l in open(path, encoding="utf-8"):
        if l.startswith("```"):
            infence = not infence
        if infence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", l)
        if m:
            s = m.group(2).strip().lower()
            s = re.sub(r"[^\w\- ]", "", s).replace(" ", "-")
            out.add(s)
    return out


diff = subprocess.run(["git", "-C", repo, "diff", "-U0", base, "HEAD", "--", page], capture_output=True, text=True).stdout
added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
own = slugs(os.path.join(repo, page))
bad = n = 0
for l in added:
    for tgt, frag in re.findall(r"\]\(([^)#]*)#([^)]+)\)", l):
        n += 1
        if tgt == "":
            ok = frag in own
        elif tgt.startswith("http"):
            continue
        else:
            ok = frag in slugs(os.path.normpath(os.path.join(repo, os.path.dirname(page), tgt)))
        if not ok:
            bad += 1
            print("UNRESOLVED", tgt, frag)
print(f"fragment links on added lines: {n}, unresolved: {bad}")
sys.exit(1 if bad else 0)
