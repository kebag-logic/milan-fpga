#!/usr/bin/env python3
"""Spot-check public source receipts and their unchanged dependencies at the reviewed head."""
import json
import re
import subprocess
import sys
from pathlib import Path

repo, packet = map(Path, sys.argv[1:3])
public = packet / 'scratch/public/adp970-r2/author/receipts/milan'
paths = ['sw/firmware/ctrl/adp', 'sw/firmware/ctrl/plat', 'sw/firmware/ctrl/test/test_adp.cpp',
         'sw/firmware/ctrl/test/test_plat_boot.cpp', 'sw/firmware/ctrl/test/ctrl_aecp_image.c',
         'third_party/tsn-c-stack', 'hdl', 'sw/mailbox', 'sw/litex',
         'tb/verilator/ctrl_service_budget/build.py', 'tb/verilator/ctrl_service_budget/grade.py',
         'tb/verilator/ctrl_service_budget/fixture.log', 'tb/verilator/ctrl_service_budget/oracle.json',
         'tb/verilator/ctrl_service_budget/selftest.py']
for path in paths:
    subprocess.run(['git', '-C', str(repo), 'diff', '--exit-code', 'f4833e16..HEAD', '--', path], check=True)
    print('UNCHANGED', path)
arms = re.findall(r"=== (\w+): Outcome\(arm='[^']+', rc=(\d+)", (public / 'arms.log').read_text())
assert arms == [('adp', '0'), ('portable', '0'), ('unit', '0'), ('walk', '0'), ('platboot1', '0'), ('platboot2', '0')]
print('Published ADP arms at preceding head:', arms)
gate = (public / 'gate.log').read_text()
for line in gate.splitlines():
    if 'C0 LINK_UP' in line or '== ctrl ADP slice' in line or 'gate rc=' in line:
        print('Published gate:', line.strip())
assert re.search(r'C0 LINK_UP[^\n]*12 accesses \(bound 12\)', gate)
assert (public / 'bselftest.log').read_text().endswith('self-test: 0 failures\nrc=0\n')
print('Published budget self-test: 0 failures, rc=0')
for name, paired, misses in [('1x1', 75, 0), ('8x8', 90, 7)]:
    cmp = (public / f'cmp-{name}.txt').read_text()
    assert f'paired {paired} probes, 0 only in base, 0 only in head' in cmp
    assert f'base misses: {misses}' in cmp and f'head misses: {misses}' in cmp
    print(f'Published CPU comparison {name}: {paired} paired; {misses} base and head misses')
    for line in (public / f'res-r5-{name}.log').read_text().splitlines():
        if 'groups graded,' in line or line == 'rc=0':
            print('Published execution:', line)
print('Prior execution is carried only through unchanged runtime, inputs and grading dependencies.')
print('No round-6 author packet or independent signature was available in the inspected evidence branch.')
print('No manager source bank or current-dev candidate execution is asserted.')
