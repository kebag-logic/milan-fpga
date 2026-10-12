#!/usr/bin/env python3
"""R624-6: rows whose receipt is the findings page at the head (FIND_P / repo:...BENCH.md): where does the
receipt text they read lie? A row is circular if every match of its pattern lies inside the covered text
(lane B16's section, from its heading to the end of the page), i.e. it reads the figure it checks.

usage: audit_self_receipts.py <check_b16_figures.py> <findings page> <out.json>"""
import ast, json, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
page = open(sys.argv[2], encoding="utf-8").read()
start = page.index("\n## Dev 5603c353, 2026-10-12: lane B16") + 1
tsv = next(n.value.value for n in ast.parse(src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "ROWS_TSV")
out, prev = [], None
for x in tsv.strip("\n").splitlines():
    if not x or x.startswith("#"):
        continue
    line, shown, s, spec, key = x.split("\t", 4)
    s = prev if s == "^" else s; prev = s
    if "FIND_P" not in key and "629_MEDIA_CLOCK_FOLLOWING_BENCH" not in key and "BENCH.md" not in s:
        continue
    pats = [n.value for n in ast.walk(ast.parse(key, mode="eval")) if isinstance(n, ast.Constant) and isinstance(n.value, str) and ("\\" in n.value or "(" in n.value)]
    where = []
    for p in pats:
        try:
            for m in re.finditer(p, page, re.M):
                where.append(page.count("\n", 0, m.start()) + 1)
        except re.error:
            pass
    inside = [w for w in where if page.count("\n", 0, start) + 1 <= w]
    out.append(dict(line=line, shown=shown, key=key[:160], match_lines=where[:6], all_inside_covered=bool(where) and len(inside) == len(where), git_receipt=("git:" in key) or ("was(" in key)))  # was() reads the page at an earlier commit (default e20fd282)
circ = [o for o in out if o["all_inside_covered"] and not o["git_receipt"]]
json.dump(dict(rows=len(out), circular=circ, all=out), open(sys.argv[3], "w"), indent=1)
print(len(out), "page-receipt rows;", len(circ), "match only inside the covered text")
for c in circ: print(c)
