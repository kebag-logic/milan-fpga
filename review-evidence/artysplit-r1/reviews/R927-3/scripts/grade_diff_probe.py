"""Disposable probe: regrade one case manifest and list the leaf paths where the result differs from the recorded
original grade. usage: python3 -E -s grade_diff_probe.py TOOLS_DIR CASE_MANIFEST"""
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import receipt_regrade as rr, grade, shape_costs
path = Path(sys.argv[2]); m = json.loads(path.read_text()); d = path.parent
L = rr.EXTRACT_PART_LIMIT
group = rr.group_from(json.loads(rr.read_parts(d, m['group'], L)))
text = rr.read_parts(d, m['extract'], L).decode()
expected = json.loads(rr.read_parts(d, m['grade'], L))
journal = None
with tempfile.TemporaryDirectory() as tmp:
    if m.get('journal'):
        journal = Path(tmp) / 'j.bin'; journal.write_bytes(bytes.fromhex(rr.read_parts(d, m['journal'], L).decode()))
    got = json.loads(json.dumps(grade.grade(text, group, m['sys_hz'], m['cpu_hz'], shape_costs.Shape(*m['shape']), journal)))
def walk(a, b, p=''):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            yield from walk(a.get(k), b.get(k), f'{p}/{k}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, f'{p}[{i}]')
    elif a != b:
        yield p, a, b
diffs = list(walk(expected, got))
for p, a, b in diffs[:40]:
    print(f'DIFF {p}: recorded={str(a)[:120]} regraded={str(b)[:120]}')
print(f'RESULT differing_leaves={len(diffs)}')
