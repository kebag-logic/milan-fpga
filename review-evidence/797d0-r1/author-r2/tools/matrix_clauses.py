#!/usr/bin/env python3
"""Check every clause and table a MILAN_COMPLIANCE_MATRIX row cites against the standard its section names.

Usage: python3 -I matrix_clauses.py <tree> <std-dir>

The page's numbered sections each cover one standard; a row's first cell
lists clause numbers ("5.4.2.5 / .6" expands the short form against the
previous number), tables and figures. Each is looked up as a heading (a line
starting with the number) or a "Table N-M" caption in that standard's text,
soft hyphens normalised. Prints one line per row: OK or the missing items.
"""
import re
import sys
from pathlib import Path

tree, std = Path(sys.argv[1]), Path(sys.argv[2])
FILES = {"1.": ["milan-1.2.txt"], "2.": ["1722.1-2021.txt"], "3.": ["1722-2016.txt"],
         "4.": ["802.1AS-2011.txt", "802.1AS-2011_Cor1-2013.txt", "802.1AS-2011_Cor_2-2015.txt"],
         "5.": ["802.1Q-2014.txt"]}
index = {}
for key, files in FILES.items():
    heads, tabs = set(), set()
    for f in files:
        text = (std / f).read_text(errors="replace").replace("­", "-")
        heads |= set(re.findall(r"(?m)^\s*(\d+(?:\.\d+)*)\.?\s+\S", text))
        heads |= set(re.findall(r"(?m)^\s*(?:Annex\s+)?([A-Z](?:\.\d+)+)\.?\s+\S", text))
        tabs |= set(re.findall(r"(Table|Figure)\s+([A-Z0-9]+[-.]\d+)", text))
    index[key] = (heads, {f"{k} {n.replace('.', '-')}" for k, n in tabs} | {f"{k} {n}" for k, n in tabs})
section = None
rows = bad = 0
for n, line in enumerate((tree / "docs/reference/MILAN_COMPLIANCE_MATRIX.md").read_text().split("\n"), 1):
    m = re.match(r"^## (\d\.)", line)
    if m:
        section = m.group(1) if m.group(1) in FILES else None
        continue
    if not section or not line.startswith("| ") or line.startswith("|---") or line.startswith("| Clause"):
        continue
    first = line.split("|")[1].strip()
    if not re.search(r"\d", first):
        continue
    heads, tabs = index[section]
    items, last = [], None
    for tok in re.findall(r"(?:Table|Figure)\s+[A-Z0-9]+[-.]\d+|\d+(?:\.\d+)+|\.\d+|\b\d+\b|[A-Z]\.\d+(?:\.\d+)*", first):
        if tok.startswith(("Table", "Figure")):
            items.append(("tab", tok))
        elif tok.startswith(".") and last:
            items.append(("head", last.rsplit(".", 1)[0] + tok))
        else:
            items.append(("head", tok))
            last = tok
    missing = []
    for kind, item in items:
        if kind == "tab":
            kind_word, num = item.split(None, 1)
            if f"{kind_word} {num}" not in tabs and f"{kind_word} {num.replace('.', '-')}" not in tabs:
                missing.append(item)
        elif item not in heads and not item.endswith(".x"):
            missing.append(item)
    rows += 1
    bad += bool(missing)
    print(f"{n}\t{'OK' if not missing else 'MISSING ' + ', '.join(missing)}\t{first}")
print(f"{rows} rows, {bad} with a clause or table not found")
