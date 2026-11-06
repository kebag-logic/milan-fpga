#!/usr/bin/env python3
"""The optional case for the rule's `any`: the positive case given a row of another path beside its own, tried on a
copy. The head must pass it and `any` turned to `all` must fail it.

usage: all_fix_feasibility.py <tree extracted at the exact head>
"""
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_hooks'
OLD = "    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [again]})\n    expect(not got['refusals']"
NEW = ("    near = dict(again, probe='hooks-disc-aging.available.if1', path=['acmp.entity_available', 1])\n"
       "    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [near, again]})\n    expect(not got['refusals']")
RULE = "if by and any((x['group'], x['path'], x['interface']) == (by, *r['path']) for x in rows):"
for name, flip in (('the case added, the rule as at the head', False), ('the case added, any turned to all', True)):
    copy = SRC.parent / 'probe_all'
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(SRC, copy, ignore=shutil.ignore_patterns('__pycache__'))
    p = copy / 'hooks_selftest.py'
    t = p.read_text()
    assert t.count(OLD) == 1
    p.write_text(t.replace(OLD, NEW))
    if flip:
        p = copy / 'run.py'
        t = p.read_text()
        assert t.count(RULE) == 1
        p.write_text(t.replace(RULE, RULE.replace('any(', 'all(')))
    out = subprocess.run([sys.executable, '-B', str(copy / 'hooks_selftest.py')], capture_output=True, text=True)
    shutil.rmtree(copy)
    lines = out.stdout.splitlines()
    print(f'{name} | rc={out.returncode} | {lines[-1]}')
    print(*[f'    {x[:120]}' for x in lines if x.startswith('FAIL ') or 'ESCAPED' in x], sep='\n')
