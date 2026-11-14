#!/usr/bin/env python3
"""Compare a costs.txt receipt (cycles at 100 MHz) with load_grade.py's STATED_US / STATED_US_DONOR, read by ast (not executed).
Usage: costs_vs_stated.py <load_grade.py> <point> <costs.txt>"""
import ast, re, sys, math
src = open(sys.argv[1]).read(); point = sys.argv[2]
tables = {}
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('STATED_US', 'STATED_US_DONOR'):
        tables[node.targets[0].id] = ast.literal_eval(node.value)
alias = {'item.aecp': 'item.aecp.notice'}
for line in open(sys.argv[3]):
    m = re.match(r'\S+\s+(\S+)\s+most\s+([\d,]+) CPU cycles, stated\s+(\d+) us; (.*)', line)
    if not m: continue
    key, cyc, rule, where = m.group(1), int(m.group(2).replace(',', '')), int(m.group(3)), m.group(4)
    us = cyc / 100.0
    out = []
    for t in ('STATED_US', 'STATED_US_DONOR'):
        v = tables[t][point].get(alias.get(key, key))
        if v is None: out.append(f'{t}=-'); continue
        flag = 'BELOW-MEAS' if v < us else ('below-rule' if v < rule else 'ok')
        out.append(f'{t}={v}:{flag}')
    print(f'{key:22s} meas {us:8.2f} rule {rule:5d}  ' + '  '.join(out) + f'  ({where})')
