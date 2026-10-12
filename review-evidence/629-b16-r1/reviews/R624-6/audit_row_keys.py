#!/usr/bin/env python3
"""R624-6: classify every figures-check row key without executing the check.

usage: audit_row_keys.py <check_b16_figures.py> <out.json>
Extracts the ROWS_TSV literal with ast, splits rows as parse_rows() does, and parses each key with ast.
A key is 'literal' if it holds no Name node (it cannot depend on any receipt or file)."""
import ast, json, sys
src = open(sys.argv[1], encoding="utf-8").read()
tsv = next(n.value.value for n in ast.parse(src).body
           if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "ROWS_TSV")
rows, lit, names, receipts = [], [], {}, {}
prev = None
for x in tsv.strip("\n").splitlines():
    if not x or x.startswith("#"):
        continue
    line, shown, s, spec, key = x.split("\t", 4)
    s = prev if s == "^" else s
    prev = s
    rows.append((line, shown, s, spec, key))
    ns = {n.id for n in ast.walk(ast.parse(key, mode="eval")) if isinstance(n, ast.Name)}
    if not ns:
        lit.append(dict(line=line, shown=shown, receipt=s, key=key))
    for n in ns:
        names[n] = names.get(n, 0) + 1
json.dump({"rows": len(rows), "literal_keys": lit,
           "names_used": dict(sorted(names.items(), key=lambda x: -x[1]))},
          open(sys.argv[2], "w"), indent=1)
print(len(rows), "rows;", len(lit), "literal keys")
