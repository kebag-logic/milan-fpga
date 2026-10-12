#!/usr/bin/env python3
"""Audit the figures check's ROWS_TSV: list rows whose key reads no receipt (a literal or constant
expression), rows on a git: receipt (superseded figures), and the EXCLUDE categories with their counts.

usage: audit_rows.py <check_b16_figures.py> <coverage.tsv>
"""
import ast
import collections
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
block = re.search(r'ROWS_TSV = r"""\n(.*?)"""', src, re.S).group(1)
rows = [l.split("\t") for l in block.splitlines() if l and not l.startswith("#")]
print("rows", len(rows))
lit, gitrows = [], []
for r in rows:
    line, shown, rec, prec, key = (r + [""] * 5)[:5]
    try:
        tree = ast.parse(key, mode="eval")
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        calls = any(isinstance(n, ast.Call) for n in ast.walk(tree))
    except SyntaxError:
        names, calls = {"?"}, True
    if not names and not calls:
        lit.append(r)
    if rec.startswith("git:") or "was(" in key:
        gitrows.append(r)
print("literal-key rows", len(lit))
for r in lit:
    print("  LIT", "\t".join(r))
print("superseded (git/was) rows", len(gitrows))
cov = collections.Counter(l.split("\t")[2] for l in open(sys.argv[2]).read().splitlines()[1:] if l)
print("coverage categories")
for k, v in cov.most_common():
    print(" ", v, k)
