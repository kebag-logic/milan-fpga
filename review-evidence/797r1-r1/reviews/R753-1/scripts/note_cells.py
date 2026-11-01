#!/usr/bin/env python3
"""Measure prose carried in one-column '| Note |' tables and in description cells.
Usage: note_cells.py <page>. The doc-style limit is 20 words a paragraph."""
import re, sys, statistics
lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
notes, desc, i = [], [], 0
while i < len(lines):
    if lines[i].strip() in ("| Note |", "| Topic | Note |"):
        i += 2
        while i < len(lines) and lines[i].startswith("|"):
            notes.append((i + 1, len(re.sub(r"[|`*]", " ", lines[i]).split())))
            i += 1
        continue
    if re.match(r"^\| \d+(:\d+)? \| `", lines[i]):
        cells = re.split(r"(?<!\\)\|", lines[i].strip().strip("|"))
        desc.append((i + 1, len(cells[-1].split())))
    i += 1
words = [w for _, w in notes]
print("Note rows", len(notes), "total words", sum(words), "median", statistics.median(words), "max", max(words))
print("Note rows over 20 words", sum(w > 20 for w in words), "over 100", sum(w > 100 for w in words), "over 300", sum(w > 300 for w in words))
print("largest Note rows (line, words):", sorted(notes, key=lambda x: -x[1])[:8])
print("field description cells over 20 words", sum(w > 20 for _, w in desc), "of", len(desc))
total = sum(len(l.split()) for l in lines)
print("page words", total, "share in Note rows %.0f%%" % (100 * sum(words) / total))
