#!/usr/bin/env python3
"""Check that every in-file '#anchor' link in a Markdown file resolves to a
heading slug (GitHub-style), and that the Contents list order matches the
heading order. Usage: check_md_anchors.py FILE [FILE...]"""
import re
import sys


def slug(text):
    s = text.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def check(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    slugs, order, seen, fence = [], [], {}, False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            base = slug(m.group(2))
            n = seen.get(base, 0)
            seen[base] = n + 1
            s = base if n == 0 else f"{base}-{n}"
            slugs.append(s)
            order.append(s)
    links = re.findall(r"\]\(#([^)]+)\)", "\n".join(lines))
    bad = [a for a in links if a not in slugs]
    toc = [a for a in links if a in slugs]
    toc_order = [s for s in order if s in toc]
    first_seen = list(dict.fromkeys(toc))
    print(f"{path}: headings={len(slugs)} links={len(links)} unresolved={len(bad)}")
    for a in bad:
        print(f"  UNRESOLVED #{a}")
    if first_seen != toc_order:
        print("  ORDER differs between link list and heading order")
    else:
        print("  order: link list matches heading order")
    return 1 if bad else 0


rc = 0
for p in sys.argv[1:]:
    rc |= check(p)
sys.exit(rc)
