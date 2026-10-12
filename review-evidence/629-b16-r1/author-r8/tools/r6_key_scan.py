#!/usr/bin/env python3
"""Lane B16, round 6: every row key of check_b16_figures.py that loops over cases uses its loop variable.

usage: r6_key_scan.py <check_b16_figures.py> <out.json>

R624-5-F1 found one row whose key looped over B-CRF and B-AAF but read B-AAF's receipt for both: the spec
had filled the loop variable in when it was built. This parses every key in ROWS_TSV as a Python expression
and lists each comprehension whose target names none of the names its body reads (an f-string's fields
count). It reads only the check. Nothing on the bench is read or written.
"""
import ast
import json
import sys

CHECK, OUT = sys.argv[1:3]
src = open(CHECK, encoding="utf-8").read()
rows = [x for x in src[src.index("# ROWS-BEGIN\n"):src.index("# ROWS-END")].splitlines()[1:] if x and not x.startswith("#")]
loops, unused = 0, []
for n, x in enumerate(rows, 1):
    key = x.split("\t", 4)[4]
    for node in ast.walk(ast.parse(key, mode="eval")):
        if isinstance(node, (ast.GeneratorExp, ast.ListComp, ast.SetComp, ast.DictComp)):
            used = {m.id for m in ast.walk(node) if isinstance(m, ast.Name) and isinstance(m.ctx, ast.Load)}
            for gen in node.generators:
                loops += 1
                target = {m.id for m in ast.walk(gen.target) if isinstance(m, ast.Name)}
                if not target & used:
                    unused.append(dict(row=n, line=x.split("\t", 1)[0], target=sorted(target), key=key))
out = dict(note="Lane B16 round 6: row keys whose loop variable is never read; offline, no bench action",
           rows=len(rows), loops=loops, unused=unused)
open(OUT, "w").write(json.dumps(out, indent=1) + "\n")
print(json.dumps(dict(rows=len(rows), loops=loops, unused=len(unused))))
sys.exit(1 if unused else 0)
