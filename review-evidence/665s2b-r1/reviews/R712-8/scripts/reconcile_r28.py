#!/usr/bin/env python3
"""Reviewer probe: the head's rows method on round 28's stated costs (load and poll tables of 66f71326), with the
corrected rules and with each earlier variant. Usage: reconcile_r28.py <repo root> <dir holding *_r28.py>"""
import ast, math, sys
from pathlib import Path
root, r28 = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_grade as r, load_grade, poll_grade
def table(path, name):
    tree = ast.parse(path.read_text())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == name for t in n.targets):
            return eval(compile(ast.Expression(n.value), str(path), 'eval'), {'dict': dict})
load_grade.STATED_US = table(r28 / 'load_grade_r28.py', 'STATED_US')
poll_grade.STATED_US = table(r28 / 'poll_grade_r28.py', 'STATED_US')
def R(): return {k: r.rows(root, '1x1/1if')[k][0] for k in ('R4', 'R5', 'R6')}
print('round 28 costs, corrected rules:', R())
rr = r.retained_retries
r.retained_retries = lambda w, p, t: min(p, math.floor(w / t) + 1)
print('  one retry fewer (floor(W/10)+1), W less the record:', R())
sw = r.srp_window; r.srp_window = lambda w, i: w
print('  one retry fewer, SRP over the whole W:', R())
r.retained_retries = rr
print('  corrected retries, SRP over the whole W:', R())
