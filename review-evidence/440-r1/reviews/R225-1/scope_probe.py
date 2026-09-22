"""Compare production ASTs, retained tests and evidence at the frozen revisions."""
import ast
import collections
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
REPO = Path('$VALIDATION_STORAGE/reviews/r225-507-r1')
BASE = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
HEAD = '0d43ff25d38917e77bb5c3d2ddb6473013cea3ba'

def functions(path):
    result = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body = node.body[1:]
            result[node.name] = ast.dump(node)
    return result

scope = {}
for name in ['gen_toc.py', 'check_em_dash.py', 'gen_toc_guards.py']:
    a = functions(OUT / 'snapshots/base/scripts' / name)
    b = functions(OUT / 'snapshots/head/scripts' / name)
    scope[name] = dict(changed=[k for k in a if a[k] != b.get(k)], added=sorted(b.keys() - a.keys()),
                       identical=sorted(k for k in a if a[k] == b.get(k)))
summary = {}
for version in ['base', 'head']:
    rows = json.loads((OUT / f'corpus-{version}.json').read_text())
    summary[version] = {}
    for mode in ['raw', 'reader']:
        counts = collections.Counter('agree' if r[mode]['h2'] == r['renderer'] else
                                     'escape' if r[mode]['h2'] > r['renderer'] else 'withhold' for r in rows)
        counts['refused'] = sum(bool(r[mode]['refused']) for r in rows)
        summary[version][mode] = dict(counts)
a = json.loads((OUT / 'pages-base.json').read_text())
b = json.loads((OUT / 'pages-head.json').read_text())
summary['pages'] = {v: dict(count=len(a[v]), engine_differences=[k for k in a[v] if a[v][k] != b[v][k]],
                           generated=sum(b[v][k]['generated'] is not None for k in b[v])) for v in a}
for field in ['headings', 'generated']:
    summary['pages']['revision_' + field + '_differences'] = [k for k in b['base'] if b['base'][k][field] != b['head'][k][field]]
a = json.loads((OUT / 'controls-base.json').read_text())
b = json.loads((OUT / 'controls-head.json').read_text())
summary['control_counts'] = {v: len(a[v]) for v in a}
summary['control_changes'] = {v: [[x, y] for x, y in zip(a[v], b[v]) if x != y] for v in a if a[v] != b[v]}
summary['runtime_ast'] = scope
summary['changed_paths'] = subprocess.check_output(['git', '-C', str(REPO), 'diff', '--name-status', BASE, HEAD], text=True)
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
