#!/usr/bin/env python3
"""Compare every delimited table block on the findings page with the published tables.md.

Usage: compare_tables.py <page.md> <tables.md>
Prints each page block's name and whether it is byte-equal to the generated block,
and the generated blocks the page does not quote.
"""
import re, sys
B = re.compile(r"<!-- table: ([a-z0-9-]+) -->\n(.*?)<!-- end table: \1 -->", re.S)
page = dict(B.findall(open(sys.argv[1]).read())); gen = dict(B.findall(open(sys.argv[2]).read()))
bad = 0
for n, body in page.items():
    ok = gen.get(n) == body; bad += not ok
    print(f"{'EQUAL ' if ok else 'DIFFER'} {n}")
print("generated but not quoted:", sorted(set(gen) - set(page)))
print("page blocks:", len(page), "differing:", bad)
sys.exit(1 if bad else 0)
