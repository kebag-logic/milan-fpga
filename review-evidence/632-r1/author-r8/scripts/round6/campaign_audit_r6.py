#!/usr/bin/env python3
"""The external review's campaign audit (R678-3 campaign_audit.py), pointed at
this round's receipts: for each inventory (tdm8_render_mutants.py MUTATIONS and
CLEAN_CONTROLS, gmstep_mutants.py CONTROLS) the named-kill line of every entry,
and the T647 PULLIN phases each pull-in log names with its verdict.
usage: campaign_audit_r6.py <repo-at-head> <receipts-dir> <out.json>"""
import ast
import json
import pathlib
import re
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
root = pathlib.Path(sys.argv[2]).resolve()
logs = {str(p.relative_to(root)): p.read_text(errors='replace') for p in root.rglob('*.log')}
out = {}
for path, variable in [
    ('tb/verilator/milan_dp_render/tdm8_render_mutants.py', 'MUTATIONS'),
    ('tb/verilator/milan_dp_render/tdm8_render_mutants.py', 'CLEAN_CONTROLS'),
    ('tb/verilator/milan_dp_render/tdm8_render_mutants.py', 'LEG_DEFECTS'),
    ('tb/verilator/milan_dp_gm_steps/gmstep_mutants.py', 'CONTROLS'),
]:
    tree = ast.parse((repo / path).read_text())
    node = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets))
    names = [ast.literal_eval((x.args if isinstance(x, ast.Call) else x.elts)[0])
             for x in node.elts]
    rows = []
    for name in names:
        hits = {p: [line.strip() for line in text.splitlines() if name in line and '[PASS]' in line]
                for p, text in logs.items()}
        fails = {p: [line.strip() for line in text.splitlines() if name in line and '[FAIL]' in line]
                 for p, text in logs.items()}
        rows.append({'entry': name,
                     'pass_lines': {p: v for p, v in hits.items() if v},
                     'fail_lines': {p: v for p, v in fails.items() if v}})
    key = f'{path}:{variable}'
    out[key] = rows
    ok = sum(bool(r['pass_lines']) and not r['fail_lines'] for r in rows)
    print(f'{key}: {len(rows)} entries; {ok} with a [PASS] line and no [FAIL] line')
    for r in rows:
        tag = 'RECORDED' if r['pass_lines'] and not r['fail_lines'] else 'MISSING '
        print(f'  {tag} {r["entry"]}')
pullin = {}
for p, text in logs.items():
    phases = sorted(set(re.findall(r'T647 PULLIN (\+\d+)', text)))
    if phases:
        res = re.findall(r'RESULT: (PASS|FAIL)', text)
        tally = re.findall(r'checks: *(\d+) +failures: *(\d+)', text)
        pullin[p] = {'phases': phases, 'result': res[-1] if res else None,
                     'tally': tally[-1] if tally else None}
print('T647 PULLIN phases named per log:')
for p in sorted(pullin):
    print(f'  {p}: {pullin[p]}')
out['pullin'] = pullin
pathlib.Path(sys.argv[3]).write_text(json.dumps(out, indent=2) + '\n')
