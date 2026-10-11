#!/usr/bin/env python3
"""Check every same-page fragment link ](#frag) in the named Markdown files
resolves to a heading slug (GitHub rule: lowercase, drop punctuation other
than '-' and '_', spaces to '-', duplicates suffixed -1, -2 ...).

usage: python3 -I intra_anchors.py <file>...
"""
import re
import sys

bad = 0
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    body = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    slugs, seen = set(), {}
    for h in re.findall(r"^#{1,6} +(.+?) *#*$", body, re.M):
        s = re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        slugs.add(s if n == 0 else f"{s}-{n}")
    links = re.findall(r"\]\(#([^)\s]+)\)", body)
    missing = sorted({l for l in links if l not in slugs})
    bad += len(missing)
    print(f"{path}: {len(links)} same-page fragment link(s), {len(missing)} unresolved {missing if missing else ''}")
sys.exit(1 if bad else 0)
