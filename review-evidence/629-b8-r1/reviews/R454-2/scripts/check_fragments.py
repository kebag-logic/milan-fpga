#!/usr/bin/env python3
"""Resolve every fragment link in the B8 section (in-page and relative-page)
against the headings of the target page, slugged the way GitHub does
(lowercase, punctuation other than '-' and '_' dropped, spaces to '-').

usage: check_fragments.py REPO_ROOT
"""
import os, re, sys

root = sys.argv[1]
page = os.path.join(root, "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md")

def slugs(path):
    out, fence = set(), False
    for line in open(path, encoding="utf-8"):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            t = re.sub(r"`", "", m.group(2)).lower()
            t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
            base, n = t, 1
            while t in out:
                t = f"{base}-{n}"; n += 1
            out.add(t)
    return out

text = open(page, encoding="utf-8").read()
sec = text[text.index("## Dev bbf704ec, 2026-10-03: lane B8"):]
bad = 0
for target, frag in re.findall(r"\]\(([^)#\s]*)#([^)\s]+)\)", sec):
    if target.startswith("http"):
        print("EXT " + target + "#" + frag + " (checked against the issue's comment ids separately)")
        continue
    tp = page if not target else os.path.normpath(os.path.join(os.path.dirname(page), target))
    ok = os.path.exists(tp) and frag in slugs(tp)
    bad += not ok
    print(("OK  " if ok else "BAD ") + (target or "(this page)") + "#" + frag)
print("bad:", bad)
sys.exit(1 if bad else 0)
