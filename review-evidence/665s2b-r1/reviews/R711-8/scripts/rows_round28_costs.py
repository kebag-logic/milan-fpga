"""Reviewer check (R711-8): the head's rows model on round 28's stated costs (66f71326's load_grade/poll_grade tables),
to split R4's move from round 28 into the rule's part and the restated costs' part. Run from the head's
tb/verilator/ctrl_service_budget: python3 -B <this>."""
import ast, subprocess, sys
from pathlib import Path
sys.path.insert(0, '.')
import load_grade as L, poll_grade as PG, rows_grade as r
root = Path('../../..').resolve()
def table(rev, path, name):
    src = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True, check=True, cwd=root).stdout
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == name for t in node.targets):
            return eval(compile(ast.Expression(node.value), name, "eval"), {"dict": dict})
base = 'tb/verilator/ctrl_service_budget/'
head = {pt: r.rows(root, pt) for pt in r.POINTS}
L.STATED_US = table('66f71326', base + 'load_grade.py', 'STATED_US')
PG.STATED_US = table('66f71326', base + 'poll_grade.py', 'STATED_US')
for pt in r.POINTS:
    old = r.rows(root, pt)
    print(pt, ' '.join(f'{row} {old[row][0]} (head costs {head[pt][row][0]})' for row in r.SOLVED))
    w, d = old['R4']
    print('  R4 terms on round 28 costs:', {k: round(v, 3) for k, v in d.items()})
