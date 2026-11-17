#!/usr/bin/env python3
"""Compare moved plant/variant definitions before and after the final refactor.
Usage: python3 -B check_refactor.py CHECKOUT
"""
import dataclasses
import subprocess
import sys
import types
from pathlib import Path

root = Path(sys.argv[1]).resolve()
def load(path, revision, name):
    source = subprocess.check_output(['git', '-C', str(root), 'show', f'{revision}:{path}']).decode()
    module = types.ModuleType(name)
    module.__file__ = str(root / path)
    sys.modules[name] = module
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    return module
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
before = load('sw/firmware/ctrl/test/aecp_mutants.py', 'd1aa4c44^', 'aecp_before')
after = load('sw/firmware/ctrl/test/aecp_mutants.py', 'd1aa4c44', 'aecp_after')
assert {d.name: dataclasses.asdict(d) for d in before.DEFECTS} == {
    d.name: dataclasses.asdict(d) for d in after.DEFECTS}
after.controls()
print(f'PASS: all {len(after.DEFECTS)} AECP plant definitions and named checks preserved; full table controls pass')
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
before = load('tb/verilator/ctrl_service_budget/build.py', 'd1aa4c44^', 'build_before')
after = load('tb/verilator/ctrl_service_budget/build.py', 'd1aa4c44', 'build_after')
assert before.MUTATIONS == after.MUTATIONS
assert before.VARIANTS == after.VARIANTS
import talker_notice
assert before.DECLARED_CONTROLS == talker_notice.CONTROLS
print(f'PASS: all {len(after.MUTATIONS)} build mutation definitions and {len(after.VARIANTS)} fixture variants preserved')
changed = subprocess.check_output(['git', '-C', str(root), 'diff', '--name-only', 'd1aa4c44^', 'd1aa4c44']).decode().splitlines()
assert not any(p.endswith(('.c', '.h', '.sv', '.json')) for p in changed)
print('PASS: final refactor changes no C/headers, RTL, or JSON limits')
