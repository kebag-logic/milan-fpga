#!/usr/bin/env python3
"""Published plant receipts, unplanted baselines, table re-render at head, and README mutant-table sync.
Usage: doc_checks.py <clone-root> <author-r2 receipts dir>"""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
root, rec = Path(sys.argv[1]), Path(sys.argv[2])
H = root / 'tb/verilator/ctrl_service_hooks'
sys.path.insert(0, str(H))
import hooks_selftest as s
run, hooks = s.run, s.hooks
readme = (H / 'README.md').read_text()
# 1. the 16 plants: the rc, the PLANT line, the path, against the unplanted row on the same path
idle = json.load(open(rec / 'runs/1x1-idle/results.json')); ans = json.load(open(rec / 'runs/1x1-ans/results.json'))
ok = 0
for name, (hook, plant) in hooks.plants().items():
    log = (rec / f'plants/plant-{name}.log').read_text()
    line = next(l for l in log.splitlines() if l.startswith('PLANT '))
    rc = re.search(r'^rc=(\d+)', log, re.M)
    base = ans if plant.arm == 'answering' else idle
    wanted = run.plant_wanted(plant)
    unplanted = run.plant_findings(plant, base['findings'])
    row = next((r for r in base['rows'] if r['probe'] == plant.probe), None) if plant.probe else None
    good = line.startswith(f'PLANT {name} caught: {wanted}:') and rc and rc.group(1) == '0' and not unplanted and (row is None or row['within'])
    in_readme = line.split('caught: ', 1)[1].split(' (')[0][:60] in readme
    ok += bool(good)
    print(f"{'ok ' if good else 'BAD'} {name:15s} rc {rc and rc.group(1)} unplanted match {len(unplanted)} unplanted row {row and (round(row['ms'],3), row['bound_ms'], row['within'])} | {line.split('caught: ')[-1][:80]} | readme {in_readme}")
print('plants ok', ok, 'of', len(hooks.plants()))
noop = (rec / 'plants/noop-counters-late.log').read_text()
print('noop:', next(l for l in noop.splitlines() if l.startswith('PLANT ')), re.findall(r'^rc=\d+', noop, re.M))
# 2. the tables re-rendered by the head's code from the published results
for n in ('1x1-idle', '1x1-ans', '8x8-idle', '8x8-ans'):
    b = json.load(open(rec / 'runs' / n / 'results.json')); spec = json.load(open(rec / 'runs' / n / 'build.json'))
    graded = {k: b[k] for k in ('rows', 'refusals', 'superseded', 'findings', 'checks')}
    text = run.table(n[:3], spec, graded)
    pub = (rec / 'runs' / n / 'table.md').read_text()
    norm = lambda t: t
    print(n, 'table.md byte-equal to the head render:', norm(text) == norm(pub), 'rows', len(b['rows']), 'note present', run.BOUNDS_NOTE in pub,
          'whole+descriptor rows in table:', len(re.findall(r'`counters\.all[.`]', pub)))
# 3. the README's mutant table against MUTANTS
names = [m[0] for m in s.MUTANTS]
tab = dict(re.findall(r'^\| ([^|]+?) \| ([^|]+?) \|$', readme.split('Then it replaces each rule in turn')[1].split('A mutant whose name ends')[0], re.M))
missing = [n for n in names if n not in tab]; extra = [n for n in tab if n not in names and n != 'Mutant' and not n.startswith('---')]
wrong = [m[0] for m in s.MUTANTS if tab.get(m[0]) != m[2]]
print('mutants', len(names), 'readme rows', len(tab) - 1 if 'Mutant' in tab else len(tab), 'missing', missing[:6], 'extra', extra[:6], 'named check differs', wrong[:6])
