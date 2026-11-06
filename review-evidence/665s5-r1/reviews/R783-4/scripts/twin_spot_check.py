#!/usr/bin/env python3
"""Three of the published twins remade independently at their source, each on a copy, with the assertion each fires.

usage: twin_spot_check.py <tree extracted at the exact head>
"""
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_hooks'
TWINS = {
    'buckets: the wait removed from both composed groups': ('hooks.py', "g.add(f'wait cycles {refilled_ms() * MS}', 'gap 1', 'mark composed')",
                                                           "g.add('gap 1', 'mark composed')", 2),
    'bound: the normative wait not added': ('run.py', "bound = hooks.bound_ms(row['family']) + row['wait_ms']",
                                            "bound = hooks.bound_ms(row['family'])", 1),
    'findings: a path over its bound fits': ('run.py', "within=not unbounded and row['ms'] <= bound, unbounded=unbounded",
                                             'within=True, unbounded=unbounded', 1),
}
for n, (name, (file, old, new, count)) in enumerate(TWINS.items()):
    copy = SRC.parent / f'probe_twin{n}'
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(SRC, copy, ignore=shutil.ignore_patterns('__pycache__'))
    p = copy / file
    t = p.read_text()
    assert t.count(old) == count, (name, t.count(old))
    p.write_text(t.replace(old, new))
    out = subprocess.run([sys.executable, '-B', str(copy / 'hooks_selftest.py')], capture_output=True, text=True)
    shutil.rmtree(copy)
    lines = (out.stdout + out.stderr).splitlines()
    print(f'{name} | rc={out.returncode}')
    for x in lines:
        if x.startswith('FAIL '):
            print('   ', x[:150])
