#!/usr/bin/env python3
"""The reviewer's hooks-counters runs at the head against the published rows; each descriptor's first and last notice from
the raw log; and a regrade of the same log with the amended constants set to absurd values.
Usage: sim_compare.py <clone-root> <author-r2 receipts dir> <sim-dir>"""
import copy, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
root, rec, sim = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import hooks_selftest as s
run, hooks, scenario, hb = s.run, s.hooks, s.scenario, s.hooks_build
for point, n in (('1x1', 'ans'), ('8x8', 'ans')):
    b = sim / f'b-{point}'
    mine = json.load(open(b / 'results/results.json'))
    pub = json.load(open(rec / f'runs/{point}-{n}/results.json'))
    spec = json.load(open(b / 'build.json'))
    pubspec = json.load(open(rec / f'runs/{point}-{n}/build.json'))
    P = {r['probe']: r for r in pub['rows'] if r['group'] == 'hooks-counters'}
    fields = ('ms', 'cpu_cycles', 'wait_ms', 'bound_ms', 'within', 'unbounded', 'margin_ms', 'slack_cycles')
    diffs = [(r['probe'], f, r[f], P[r['probe']][f]) for r in mine['rows'] for f in fields if r[f] != P[r['probe']][f]]
    print(f"{point}: my rows {len(mine['rows'])}, published rows of the group {len(P)}, same set {set(P) == {r['probe'] for r in mine['rows']}}, field diffs {len(diffs)}")
    pf = {x for x in pub['findings'] if x.endswith('(hooks-counters)')}
    print(f"   findings same {set(mine['findings']) == pf}; ELF digest same {spec['inputs']['build:image/ctrl_app.elf'] == pubspec['inputs']['build:image/ctrl_app.elf']}")
    ins = [k for k in spec['inputs'] if spec['inputs'][k] != pubspec['inputs'].get(k)]
    print('   inputs that differ from the published run:', ins)
    for d in diffs[:5]: print('   DIFF', d)
    # the raw log: each descriptor's first and last notice from the ALL change
    text = (b / 'results/hooks-counters.log').read_text()
    log, own = hooks.parsed(text, spec['sys_hz'], spec['cpu_hz'])
    pads = sorted(c for c, name, i in log.pads if name == 'CTR')
    change = pads[1]
    seen = {}
    for c, ch, i, frame in log.tx:
        if ch == scenario.CH['aecp'] and c >= change and len(frame) > 42:
            kind, index = int.from_bytes(frame[38:40], 'big'), int.from_bytes(frame[40:42], 'big')
            seen.setdefault((kind, index), []).append(c)
    want = {k: v for k, v in seen.items() if k != (5, 0)}
    order = sorted(want, key=lambda k: want[k][0])
    ms = lambda c: (c - change) / hooks.BUS_MS
    print(f"   pads {len(pads)}; the ALL change at {change}")
    lines = [(f't{k}.i{n_}', round(ms(want[(k, n_)][0]), 2), round(ms(want[(k, n_)][-1]), 2), round(ms(want[(k, n_)][-1]) - ms(want[(k, n_)][0]), 2), len(want[(k, n_)])) for k, n_ in order]
    for l in lines: print('   ', l)
    readme = (root / 'tb/verilator/ctrl_service_hooks/README.md').read_text()
    tab = readme.split(f"{point}, amended ceiling")[1].split('\n\n')[1]
    rows = {m[0]: tuple(float(x) for x in m[1:]) for m in re.findall(r'^\| `(t\d+\.i\d+)` \| ([\d.]+) \| \**([\d.]+)\** \| ([\d.]+) \|$', tab, re.M)}
    mism = [(l, rows.get(l[0])) for l in lines if rows.get(l[0]) is None or abs(rows[l[0]][0] - l[1]) > 0.0051 or abs(rows[l[0]][1] - l[2]) > 0.0051 or abs(rows[l[0]][2] - l[3]) > 0.0151]
    print(f"   README table rows {len(rows)}, order same {list(rows) == [l[0] for l in lines]}, rows differing beyond rounding {len(mism)}", mism[:3])
    # the regrade with the amended constants absurd
    p = scenario.point(point, spec)
    groups = [g for g in hooks.groups(p, spec) if g.name == 'hooks-counters']
    out = sim / f'regrade-{point}'; out.mkdir(exist_ok=True)
    logs = [b / 'results/hooks-counters.log']
    base = run.grade_all(groups, logs, spec, out)
    keep = (hooks.AMENDED_SRP_MS, dict(hooks.AMENDED_QUEUED_CEILING_MS))
    t0 = run.table(point, spec, base)
    hooks.AMENDED_SRP_MS, hooks.AMENDED_QUEUED_CEILING_MS = 1e6, {1: 1e6, 2: 1e6}
    big = run.grade_all(groups, logs, spec, out)
    t1 = run.table(point, spec, big)
    hooks.AMENDED_SRP_MS, hooks.AMENDED_QUEUED_CEILING_MS = 0.0, {1: 0.0, 2: 0.0}
    small = run.grade_all(groups, logs, spec, out)
    hooks.AMENDED_SRP_MS, hooks.AMENDED_QUEUED_CEILING_MS = keep
    print('   amended constants at 1e6 and at 0: grade identical', base == big == small, '; findings', len(base['findings']), '; table differs', t0 != t1)
    # every cell but the amended one, in both tables, is the same
    cells = lambda line: [c.strip() for c in line.split('|')]
    head0 = [n for n, c in enumerate(cells(next(l for l in t0.splitlines() if l.startswith('| Hook | Paths')))) if c.startswith('Amended')]
    head1 = [n for n, c in enumerate(cells(next(l for l in t0.splitlines() if l.startswith('| Hook | Path |')))) if c.startswith('Amended')]
    other = []
    for a_, c_ in zip(t0.splitlines(), t1.splitlines()):
        if a_ == c_:
            continue
        x, y = cells(a_), cells(c_)
        changed = [n for n in range(len(x)) if x[n] != y[n]]
        if changed not in ([head0[0]], [head1[0]]):
            other.append(a_[:60])
    print('   table lines that differ', sum(a_ != c_ for a_, c_ in zip(t0.splitlines(), t1.splitlines())), 'of', len(t0.splitlines()), '; lines differing in any other cell:', other)
