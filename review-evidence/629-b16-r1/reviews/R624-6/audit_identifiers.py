#!/usr/bin/env python3
"""R624-6: list every identifier the figures check used to cover digits, with the text that follows it on
its source line, so a reader can judge whether any identifier stands for a measurement.

usage: audit_identifiers.py <coverage.tsv> <findings page> <out.tsv>
For each coverage line (line, identifier, category) it finds the identifier on that source line (each
occurrence in turn) and records the 48 characters after it. Output is grouped by category."""
import sys, collections
cov, page, out = sys.argv[1:4]
lines = open(page, encoding="utf-8").read().split("\n")
readme = open(page.rsplit("/", 1)[0] + "/README.md", encoding="utf-8").read().split("\n")
seen = collections.Counter()
rows = []
for x in open(cov, encoding="utf-8"):
    if x.startswith("#"):
        continue
    f = x.rstrip("\n").split("\t")
    if len(f) < 3:
        continue
    ln, ident, cat = f[0], f[1], f[2]
    src = readme if ln.startswith("README") else lines
    n = int(ln.split(":")[-1])
    text = src[n - 1] if 0 < n <= len(src) else ""
    k = seen[(ln, ident)]
    seen[(ln, ident)] += 1
    pos, i = -1, 0
    while i <= k:
        pos = text.find(ident, pos + 1)
        if pos < 0:
            break
        i += 1
    after = text[pos + len(ident):pos + len(ident) + 48] if pos >= 0 else "<not on line: block spans lines>"
    rows.append((cat, ln, ident, after))
rows.sort()
with open(out, "w", encoding="utf-8") as o:
    o.write("category\tline\tidentifier\tfollowing text\n")
    for r in rows:
        o.write("\t".join(r) + "\n")
print(len(rows), "identifiers listed")
