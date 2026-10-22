#!/usr/bin/env python3
"""Compare changed campaign inventories with the published execution receipts."""
import ast
import json
import pathlib
import re
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(__file__).resolve().parent
root = packet / 'scratch/published'
logs = {str(p.relative_to(root)): p.read_text(errors='replace')
        for p in root.rglob('*.log')
        if str(p.relative_to(root)).startswith(('round4/', 'round5/'))}
out = {}
for path, variable in [
    ('tb/verilator/milan_dp_render/tdm8_render_mutants.py', 'MUTATIONS'),
    ('tb/verilator/milan_dp_gm_steps/gmstep_mutants.py', 'CONTROLS'),
]:
    tree = ast.parse((repo / path).read_text())
    node = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets))
    names = [ast.literal_eval((x.args if isinstance(x, ast.Call) else x.elts)[0])
             for x in node.elts]
    rows = []
    for name in names:
        hits = {p: [line for line in text.splitlines()
                    if name in line and '[PASS]' in line
                    and ('mutant caught' in line or 'control caught' in line)]
                for p, text in logs.items()}
        hits = {p: lines for p, lines in hits.items() if lines}
        rows.append({'control': name, 'receipts': hits})
    out[path] = rows
    print(path, ':', len(rows), 'inventory entries;', sum(bool(r['receipts']) for r in rows),
          'with named PASS execution receipts after queue replacement')
    for r in rows:
        print(('  RECORDED ' if r['receipts'] else '  MISSING  ') + r['control'])
pullin = {}
for p, text in logs.items():
    phases = sorted(set(re.findall(r'T647 PULLIN (\+\d+)', text)))
    if phases:
        pullin[p] = phases
print('Shipping T647 PULLIN phases named in logs:', json.dumps(pullin, sort_keys=True))
out['pullin_phases'] = pullin
(packet / 'campaign-audit.json').write_text(json.dumps(out, indent=2) + '\n')
