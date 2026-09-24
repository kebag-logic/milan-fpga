#!/usr/bin/env python3
"""Classify every line of a `pdftotext -layout` extraction of IEEE 802.1AS-2011
that names delayAsymmetry, by the clause region it falls in. Line numbers are
newline-based, as grep counts them (form feeds at page breaks do not split).
Region bounds are the extraction lines of the clause headings in that file.
Usage: classify_asym_lines.py <802.1AS-2011.txt>"""
import collections
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read().split("\n")
REGIONS = (  # (first line NOT in region, label)
    (2200, "8.3 definition"),
    (3810, "10.2.4.8 definition"),
    (4700, "10.2.12 Figure 10-9 ARITHMETIC"),
    (7000, "11.1.3 prose"),
    (7300, "11.2.5 prose (link aggregation)"),
    (7420, "11.2.13.2.1 f) ARITHMETIC and its NOTEs"),
    (8500, "Table 11-5 prose"),
    (11100, "14.6.9 definition"),
    (11300, "Table 14-6 management"),
    (15000, "Clause 15 MIB management"),
    (17000, "unclassified"),
    (10**9, "Annex E.5.2 CSN (TLV field E.5.2.1.1.9; E.5.2.2 ARITHMETIC input)"),
)
hits = [i + 1 for i, line in enumerate(text) if re.search("delayasymmetry", line, re.I)]
label = {n: next(c for lim, c in REGIONS if n < lim) for n in hits}
print(f"lines naming delayAsymmetry: {len(hits)}")
for c, v in sorted(collections.Counter(label.values()).items()):
    print(f"{v:3d}  {c}: {[n for n in hits if label[n] == c]}")
unc = [n for n in hits if label[n] == "unclassified"]
print("unclassified:", unc)
sys.exit(1 if unc else 0)
