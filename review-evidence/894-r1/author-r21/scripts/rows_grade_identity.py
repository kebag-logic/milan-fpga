#!/usr/bin/env python3
"""rows_grade.py at BASE (a git rev) against the tree's: the part of its docstring documented() parses (after 'Sources,
and their arrival bound'), documented()'s sources, and the AST without the module docstring, positions included.
Exits 1 on any difference. Run from the tree's top. usage: rows_grade_identity.py BASE"""
import ast
import re
import subprocess
import sys

F = 'tb/verilator/ctrl_service_budget/rows_grade.py'
a = subprocess.run(['git', 'show', f'{sys.argv[1]}:{F}'], capture_output=True, text=True, check=True).stdout
b = open(F, encoding='utf-8').read()


def split(src):
    t = ast.parse(src)
    d = ast.get_docstring(t, clean=False)
    t.body = t.body[1:]
    return ast.dump(t, include_attributes=True), d


(sa, da), (sb, db) = split(a), split(b)
key = 'Sources, and their arrival bound'
pa, pb = da.split(key)[1], db.split(key)[1]
ra, rb = (set(re.findall(r'^  ([a-z]+) {2,}', x, re.M)) for x in (pa, pb))
print(f'# {F}, {sys.argv[1]} against the tree')
print(f'the part documented() parses identical: {pa == pb} ({len(pb)} characters)')
print(f'documented() identical: {ra == rb} {sorted(rb)}')
print(f'AST without the module docstring identical, positions included: {sa == sb}')
print(f'line counts: {a.count(chr(10))} and {b.count(chr(10))}')
print('docstring lines changed:', [i + 3 for i, (x, y) in enumerate(zip(da.split(chr(10)), db.split(chr(10)))) if x != y])
ok = pa == pb and ra == rb and sa == sb and a.count('\n') == b.count('\n')
print(f'RESULT: {"identical" if ok else "DIFFERS"}')
sys.exit(0 if ok else 1)
