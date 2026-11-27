"""Try extract filters against each case's recorded grade (grade.grade equality), for chosen cases."""
import json, sys, time
from pathlib import Path
root = Path.cwd()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import build, grade, run, scenario, shape_costs
CEN = Path('$VALIDATION_STORAGE/r7/final-census')
OMIT = (b'PC', b'FETCH', b'REPLY', b'TXREADY', b'FLASH')
KEEP = {b'adp_mbx:on_poll', b'ctrl_app_srp:deliver', b'acmp_mbx:on_poll', b'aecp:transmit', b'srp_mbx:reset_interface',
        b'srp_mbx:open_interface', b'srp_mbx:apply_receive', b'srp_mbx:build_mrpdu', b'acmp_rx', b'acmp_mbx:on_frame',
        b'ctrl_loop:round_of', b'aecp_command', b'aecp:finish', b'srp_mbx:receive', b'aecp_mbx:frame',
        b'mrp_attr_visit', b'mrp_reclaim'}
def extract(path):
    return [l for l in open(path, 'rb') if l.strip() and l.split(maxsplit=1)[0] not in OMIT]
def label(l):
    p = l.split(); return p[5] if p[0] == b'SPAN' else p[3]
def f1(lines):
    return [l for l in lines if not l.startswith((b'SPAN ', b'CALL ')) or label(l) in KEEP]
def f2(lines):
    # F1, and of the kept traced lines only those that start inside a work pass (PASS start_cpu .. + cycles).
    wins = []
    for l in lines:
        if l.startswith(b'PASS '):
            p = l.split(); wins.append((int(p[3]), int(p[3]) + int(p[4])))
    import bisect
    starts = [w[0] for w in wins]
    def inside(c):
        i = bisect.bisect_right(starts, c) - 1
        return i >= 0 and c <= wins[i][1]
    out = []
    for l in f1(lines):
        if l.startswith((b'SPAN ', b'CALL ')):
            if not inside(int(l.split()[2])): continue
        out.append(l)
    return out
cases = [c.split('/') for c in sys.argv[1].split(',')]
for variant, name in cases:
    spec = json.loads((CEN / variant / 'build.json').read_text()); results = CEN / variant / 'results'
    g = {x.name: x for x in run.all_groups(scenario.point('arty-1x1', spec), spec)}[name]
    expected = json.loads((results / (name + '.json')).read_text())
    j = run.journal_of(results, g) if g.save.get('journal') else None
    lines = extract(results / (name + '.log'))
    for fname, fn in (('full', lambda x: x), ('F1', f1), ('F2', f2)):
        t = time.time(); kept = fn(lines); text = b''.join(kept).decode()
        got = grade.grade(text, g, spec['sys_hz'], spec['cpu_hz'], shape_costs.Shape(1, 1, 2), j)
        same = json.loads(json.dumps(got)) == expected
        print(variant, name, fname, len(text), 'SAME' if same else 'DIFFERS', round(time.time() - t, 1), flush=True)

def diff(a, b, path=''):
    if type(a) != type(b): print('  TYPE', path); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: print('  KEY', path + '/' + str(k)); continue
            diff(a[k], b[k], path + '/' + str(k))
    elif isinstance(a, list):
        if len(a) != len(b): print('  LEN', path, len(a), len(b)); return
        for i, (x, y) in enumerate(zip(a, b)): diff(x, y, f'{path}[{i}]')
    elif a != b: print('  VAL', path, str(a)[:80], '->', str(b)[:80])
if len(sys.argv) > 2:
    variant, name = sys.argv[2].split('/')
    spec = json.loads((CEN / variant / 'build.json').read_text()); results = CEN / variant / 'results'
    g = {x.name: x for x in run.all_groups(scenario.point('arty-1x1', spec), spec)}[name]
    expected = json.loads((results / (name + '.json')).read_text())
    got = json.loads(json.dumps(grade.grade(b''.join(f2(extract(results / (name + '.log')))).decode(), g, spec['sys_hz'],
                                            spec['cpu_hz'], shape_costs.Shape(1, 1, 2), None)))
    diff(expected, got)
