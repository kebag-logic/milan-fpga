#!/usr/bin/env python3
"""Prove the regenerated page differs from the base page only by the intended columns.

Usage: page_semantic_diff.py BASE_PAGE HEAD_PAGE. Maps each base line to its expected
head form (Lines columns gone, Line cell to Located, banner wording) and reports the rest.
"""
import re
import sys

base = open(sys.argv[1], encoding="utf-8").read().split("\n")
head = open(sys.argv[2], encoding="utf-8").read().split("\n")
print("lines base/head", len(base), len(head))
split = lambda r: re.split(r"(?<!\\)\|", r)
section, mapped = "", []
for row in base:
    if row.startswith("## "):
        section = row[3:].strip()
    if row.startswith("|"):
        p = split(row)
        if section == "Summary" and len(p) == 5 and p[1].strip() in ("Status", "---", "current", "stale", "superseded", "obsolete", "**total**"):
            p = p[:3] + p[4:]
        elif section == "Summary" and p[1].startswith("---") and len(p) == 5:
            p = p[:3] + p[4:]
        elif section == "Inventory" and len(p) == 11:
            p = p[:2] + p[3:]
        elif section == "Findings" and len(p) == 8:
            cell = p[3].strip()
            if cell == "Line":
                p[3] = " Located "
            elif cell == "---:":
                p[3] = "---"
            elif cell.isdigit():
                p[3] = " on page "
        row = "|".join(p)
    row = row.replace("|---:|---:|\n", "")
    mapped.append(row)
rest = [(n + 1, a, b) for n, (a, b) in enumerate(zip(mapped, head)) if a != b]
print("lines left different after the intended mapping:", len(rest))
for n, a, b in rest[:12]:
    print(f"  line {n}\n   base: {a[:200]}\n   head: {b[:200]}")
count = lambda lines, text: sum(text in l for l in lines)
for text in ("| re-verify: quote not found |", "| on page |"):
    print(repr(text), "base", count(base, text), "head", count(head, text))
print("D0 rows base/head", count(base, "| D0-"), count(head, "| D0-"))
