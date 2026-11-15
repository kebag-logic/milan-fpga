#!/usr/bin/env python3
"""Read-only review audit. Usage: audit.py SOURCE PUBLIC_EVIDENCE OUTPUT."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

src, ev, out = map(Path, sys.argv[1:])
out.mkdir(exist_ok=True)
tmp = out / 'scratch' / 'tmp'
tmp.mkdir(parents=True, exist_ok=True)
rows = json.loads((ev / 'MANIFEST.json').read_text())
selected = [x for x in rows if re.match(r'author-r[6789]/', x['file'])]
bad = []
for x in selected:
    p = ev / x['file']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != x['published_sha256']:
        bad.append(x['file'])
print('Published manifest:', len(selected), 'checked; mismatches:', bad)
for n in (6, 7, 8, 9):
    root = ev / f'author-r{n}/receipts'
    index = root / 'INDEX.md'
    if not index.exists():
        continue
    section = ''
    checks, errors = 0, []
    for line in index.read_text().splitlines():
        if line.startswith('## '):
            section = line[3:]
        m = re.fullmatch(r'\| (.+) \| (\d+) \| `([a-f0-9]{64})` \|', line)
        if m:
            p = root / section / m[1]
            checks += 1
            if not p.exists() or len(p.read_bytes()) != int(m[2]) or hashlib.sha256(p.read_bytes()).hexdigest() != m[3]:
                errors.append(str(p.relative_to(ev)))
    print('INDEX', n, checks, 'checked; mismatches:', errors)
ident = ev / 'author-r9/receipts/identity'
names = ['head-73388996', 'merge-663b519b', 'head-449d29d2', 'final-056d619d']
maps = []
for n in names:
    maps.append(dict((line.split(' ',1)[1],line.split(' ',1)[0]) for line in (ident/f'image-sha256-{n}.txt').read_text().splitlines()))
for a,b,an,bn in zip(maps,maps[1:],names,names[1:]):
    diff = [k for k in a if a[k] != b.get(k)]
    print('Image hashes',an,bn,'sets equal',a.keys()==b.keys(),'files',len(a),'changed',len(diff))
    for k in diff:
        print(' changed',k)
assert not bad

cmds = {
 'flip-1x1': ['tb/verilator/ctrl_service_budget/flip_grade.py','--check','--point','1x1/1if'],
 'rows-selftest': ['tb/verilator/ctrl_service_budget/rows_tiers.py','--selftest'],
 'load': ['tb/verilator/ctrl_service_budget/load_grade.py','--check'],
 'grid': ['tb/verilator/ctrl_service_budget/tier_grid.py','--point','1x1/1if'],
 'harness-selftest': ['tb/verilator/ctrl_service_budget/run.py','--self-test'],
}
def run(item):
    name, args = item
    with (out/f'{name}.log').open('w') as f:
        r = subprocess.run([sys.executable,'-B',*args],cwd=src,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(tmp)})
    (out/f'{name}.rc').write_text(str(r.returncode)+'\n')
    return name,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for name,rc in pool.map(run,cmds.items()):
        print('Focused check',name,'rc',rc)
