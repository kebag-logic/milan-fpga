#!/usr/bin/env python3
"""Per-round figure comparison between two PR bodies.

Splits each body at its '## Round N' headings (text before 'Round 2' is round 1),
collects every number (1,234 groups kept together) per round, and lists the
figures of the OLD body's round that have no occurrence in the NEW body's same
round, each with the old line it came from.

usage: pr_body_figures.py OLD.md NEW.md
"""
import collections
import re
import sys

NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")


def sections(text):
    parts = re.split(r"(?m)^## (Round [0-9a-z]+)\s*$", text)
    out = {"Round 1": parts[0]}
    for i in range(1, len(parts), 2):
        out[parts[i]] = parts[i + 1]
    return out


old, new = (sections(open(p).read()) for p in sys.argv[1:3])
print("rounds old:", list(old), "new:", list(new))
for k, body in old.items():
    co, cn = collections.Counter(NUM.findall(body)), collections.Counter(NUM.findall(new.get(k, "")))
    gone = sorted((n for n in co if n not in cn), key=lambda x: (len(x), x))
    print(f"\n{k}: {sum(co.values())} figure occurrences in OLD, {sum(cn.values())} in NEW")
    print(f"  OLD figures with no occurrence in NEW {k}: {gone}")
    for n in gone:
        m = re.search(r"[^\n]{0,90}(?<![\d,])" + re.escape(n) + r"(?![\d,]\d)[^\n]{0,60}", body)
        if m:
            print(f"     {n}: ...{m.group(0).strip()[:170]}...")
