#!/usr/bin/env python3
"""Audit published mutation controls and extract parent validation tallies."""
import pathlib
import re
import runpy
import sys

P = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(sys.argv[1]).resolve()
ROOT = P / 'public-evidence/author-r2/receipts/round2'
A = ROOT / 'lane-head-2022d363/engine-mutants'
mutations = runpy.run_path(str(SRC / 'tb/verilator/engine/mutants.py'))['MUTATIONS']
checks = 0
for i, (name, fname, pattern, replacement, breaks) in enumerate(mutations):
    assert (SRC / 'hdl' / fname).read_text().count(pattern) == 1
    log = (A / f'mut-{i // 3}.log').read_text()
    assert f'[PASS] mutant caught: {name} - breaks "{breaks}"' in log, name
    if breaks.startswith(('#82 ', '#84 ', '#85 ', 'p1 255 ', 'slew:')):
        for want in breaks.split(' | '):
            assert any(want in line and line.startswith('FAIL p1 255 ') == want.startswith('p1 255 ')
                       for line in log.splitlines() if line.startswith('FAIL ')), (name, want)
            checks += 1
assert all('[PASS] the unmutated engine still passes the harness' in (A / f'mut-{i}.log').read_text()
           for i in range(24))
print(f'PASS: {len(mutations)}/72 matching source mutants caught; {checks} required named failures; 24 positive controls.')
for rel in ['lane-head-2022d363/engine-run.log',
            'parent-adoption-564466ea/06.log',
            'parent-adoption-564466ea/milan_dp/gptp.log',
            'parent-adoption-564466ea/milan_dp/gptp-lat.log',
            'parent-adoption-564466ea/milan_dp_gptp/dp-gptp-physical.log',
            'parent-adoption-564466ea/milan_dp_gm_steps/milan_dp_gm_steps.log']:
    print('\n' + rel)
    for line in (ROOT / rel).read_text().splitlines():
        if re.search(r'\d+ checks:|checks: +\d+.*failures:|grandmaster change holds|tu clears within|loss leaves this station|role is synchronised', line):
            print(line)
print('\nParent new negative controls (executed on the earlier executable-equivalent snapshot):')
for rel in ['mutants-milan_dp-gptp', 'mutants-milan_dp_gptp']:
    print(rel)
    print((ROOT / 'parent-adoption-3f053cc1' / rel / 'rc.txt').read_text())
print('The first-gm-no-hold survivor is recorded, not counted as caught; manager ruling accepts the redundant arm.')
