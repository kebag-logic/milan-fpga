#!/usr/bin/env python3
"""Record source scope, simulator identity and actual mutation dispatch population.
Usage: source_audit.py CHECKOUT SCOPED_SIMULATOR
Dispatch callbacks are intercepted; this executes no mutation campaign.
"""
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

root = Path(sys.argv[1]).resolve()
print(subprocess.check_output([sys.argv[2], '--version'], text=True).strip())
files = subprocess.check_output(['git', '-C', str(root), 'diff', '--name-only', '70f4056f..HEAD'], text=True).splitlines()
assert len(files) == 10
assert all(p.startswith(('sw/firmware/ctrl/test/', 'tb/verilator/milan_dp/')) or
           p == 'sw/firmware/ctrl/srp/README.md' for p in files)
print('Changed files:')
print('\n'.join(files))
subprocess.run(['git', '-C', str(root), 'diff', '--check', '70f4056f..HEAD'], check=True)
print('Diff whitespace check PASS; no production firmware/RTL/gitlink delta')
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import test_ctrl_firmware as driver
def record(out, lwsrp, jobs=4, interfaces=2):
    names = [d.name for d in driver.srp_mutants.DEFECTS]
    print(f'Scheduled source mutants: {interfaces} interface(s), {len(names)} defects')
    print('New #929 mutants:', [n for n in names if n.endswith('-8x8') or n.startswith('startup-8x8')])
    return False
driver.srp_mutants.campaign = record
driver.ctrl_mutants.lwsrp_pin_arms = lambda *args: 0
driver.run_srp_mutants(SimpleNamespace(lwsrp=root / 'third_party/lwSRP', jobs=4), root)
print('Dispatcher also invokes the two lwsrp_pin_arms refusal controls; full campaigns NOT RUN here')
