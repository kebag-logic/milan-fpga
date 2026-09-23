#!/usr/bin/env python3
"""Check that every intra-page (#fragment) link on a Markdown page resolves to a heading slug.

Usage: intra_page_anchors.py <page.md>
"""
import re
import sys

t = open(sys.argv[1], encoding="utf-8").read()
body = re.sub(r"```.*?```", "", t, flags=re.S)
slugs = set()
for h in re.findall(r"(?m)^#{1,6} (.+)$", body):
    s = re.sub(r"[`*_]", "", h.strip().lower())
    s = re.sub(r"[^\w\- ]", "", s).replace(" ", "-")
    slugs.add(s)
links = re.findall(r"\]\(#([^)]+)\)", t)
print(sys.argv[1], "intra-page links", len(links), "distinct", len(set(links)),
      "unresolved", [x for x in links if x not in slugs])
