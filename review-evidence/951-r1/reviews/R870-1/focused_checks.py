#!/usr/bin/env python3
"""Run from a checkout: python3 -B focused_checks.py CHECKOUT PACKET [--worker POINT]."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument('checkout', type=Path)
ap.add_argument('packet', type=Path)
ap.add_argument('--worker', choices=('1x1', '8x8'))
ap.add_argument('--jobs', type=int, default=4)
a = ap.parse_args()
root, packet = a.checkout.resolve(), a.packet.resolve()
os.environ['TMPDIR'] = str(packet / 'scratch')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
if not a.worker:
    def launch(point):
        with (packet / f'focused-{point}.log').open('w') as log:
            result = subprocess.run([sys.executable, '-B', __file__, str(root), str(packet),
                                     '--worker', point, '--jobs', str(a.jobs)], stdout=log,
                                    stderr=subprocess.STDOUT, timeout=580)
        (packet / f'focused-{point}.rc').write_text(str(result.returncode) + '\n')
        return result.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(launch, ('1x1', '8x8')))
    print('Focused suites and mutations:', results)
    sys.exit(any(results))

sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
from ctrl_build import CTRL, Tree
import fw_gtest
import srp_arms
import srp_mutants

point = a.worker
interfaces = 1 if point == '1x1' else 2
config = srp_arms.DEFAULT_ENTITY if point == '1x1' else srp_arms.ENTITY_8X8
out = packet / 'scratch' / point
tree = Tree(CTRL, out / 'clean', out / 'reuse', fw_gtest.Build(jobs=a.jobs))
failed = False
for suite in ('srp_talker.cpp', ('test_acmp_mbx.cpp', 'SrpGate.*')):
    result = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', interfaces, test=suite, config=config)
    print(result.arm, 'rc', result.rc, flush=True)
    print(result.log, flush=True)
    failed |= bool(result.rc)

names = {'talker-hold-off-one-leaveall', 'talker-hold-off-two-leavealltime-periods',
         'talker-hold-off-two-leavealltime-periods-after-a-conflict',
         'talker-hold-off-drops-the-transmit-term', 'talker-hold-off-drops-the-join-and-transmit-terms',
         'talker-hold-off-rounds-the-transmit-term-down', 'talker-hold-off-never-ends',
         'short-leave', 'latency-leave-origin', 'walk-leave-shortened'}
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
assert {d.name for d in srp_mutants.DEFECTS} == names
failed |= srp_mutants.campaign(out / 'mutants', root / 'third_party/lwSRP', jobs=a.jobs, interfaces=interfaces)
for log in sorted((out / 'mutants').glob('*.log')):
    (packet / f'{point}-{log.name}').write_bytes(log.read_bytes())
print('RESULT', 'FAIL' if failed else 'PASS', flush=True)
sys.exit(failed)
