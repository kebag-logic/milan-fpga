#!/usr/bin/env python3
"""README figures against results: the hook tables, the per-descriptor tables from this review's own runs, the mutant
table against MUTANTS, and every plant's catch rule on the real unplanted runs. args: packet scratch, evidence, clone."""
import json, re, sys
from pathlib import Path
S, ev, root = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import hooks_selftest as st, hooks, run
readme = (root / 'tb/verilator/ctrl_service_hooks/README.md').read_text().splitlines()
res = {n: json.load(open(ev / f'author-r2/receipts/runs/{n}/results.json')) for n in ('1x1-idle', '1x1-ans', '8x8-idle', '8x8-ans')}
# hook tables
bad = n = 0
for point, head in (('1x1', '1x1, CPU 100 MHz on `sys`:'), ('8x8', '8x8, CPU 100 MHz on `sys`:')):
    i = readme.index(head) + 4
    while readme[i].startswith('|'):
        c = [x.strip().strip('*') for x in readme[i].split('|')[1:-1]]
        hook = c[0]
        for col, run_n, part in ((3, f'{point}-idle', 'alone'), (4, f'{point}-ans', 'alone'), (5, f'{point}-idle', 'loaded'), (6, f'{point}-ans', 'loaded')):
            w = res[run_n]['summary'][hook]['worst'].get(part)
            want = '-' if w is None else 'never served' if w['unbounded'] else f"{w['ms']:.2f}"
            n += 1
            if want != c[col]:
                bad += 1; print('  hook table differs', point, hook, part, run_n, c[col], want)
        i += 1
print(f'hook tables: {n} cells compared, {bad} differ')
# per descriptor tables
for point, build, head in (('1x1', 'b1x1', '1x1, amended ceiling 20:'), ('8x8', 'b8x8', '8x8, amended ceiling 60:')):
    g = json.load(open(S / build / 'results/hooks-counters.json'))
    probes = {p['probe']: p for p in g['probes']}
    print(f'{point} fanout keys:', sorted(probes['counters.all.t5.i1.if0']['fanout']))
    i = readme.index(head) + 4
    rows = bad = 0
    while readme[i].startswith('|'):
        c = [x.strip().strip('*`') for x in readme[i].split('|')[1:-1]]
        p = probes[f'counters.all.{c[0]}.if0']
        f = p['fanout']
        vals = {k: v for k, v in f.items()}
        rows += 1
        if f"{p['ms']:.2f}" != c[2]:
            bad += 1; print('  row differs', c, p['ms'])
        if rows == 1: print('  sample', c, vals)
        i += 1
    print(f'{point}: {rows} rows, {bad} last-notice figures differ')
# mutant table
names = [m[0] for m in st.MUTANTS]
doc = [re.sub(r'\\\|', '|', l.split(' | ')[0].lstrip('| ').strip()) for l in readme if l.startswith('| ') and l.rstrip().endswith(' |') and any(l.startswith('| ' + x) for x in names)]
print(f'mutants: {len(names)} in the list; {len(doc)} README rows name one exactly; missing {[x for x in names if x not in doc]}')
# plant catch rules on unplanted 1x1 runs
hit = []
for name, (hook, plant) in hooks.plants().items():
    arm = '1x1-ans' if plant.arm == 'answering' else '1x1-idle'
    got = run.plant_findings(plant, res[arm]['findings'])
    if got: hit.append((name, got[:1]))
print(f'plant catch rules on the real unplanted 1x1 runs: {len(hooks.plants())} rules, {len(hit)} match', hit)
