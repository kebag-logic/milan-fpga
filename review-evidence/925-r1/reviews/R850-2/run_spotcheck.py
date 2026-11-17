#!/usr/bin/env python3
"""Run the previous reproductions and changed regressions against a supplied clone."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import ctrl_build
import fw_gtest
import srp_arms

tests = packet / 'scratch/spot-tests'
tests.mkdir(parents=True, exist_ok=True)
for suite, additions in [('srp_mbx.cpp', ['probes.cpp', 'rebind.cpp', 'reproduce.cpp']),
                         ('test_acmp_mbx.cpp', ['reproduce_feedback.cpp'])]:
    data = (repo / 'sw/firmware/ctrl/test' / suite).read_bytes()
    for addition in additions:
        data += (packet / addition).read_bytes()
    (tests / suite).write_bytes(data)
srp_arms.HERE = tests

def run(interfaces):
    out = packet / 'scratch' / f'spot-if{interfaces}'
    tree = ctrl_build.Tree(ctrl_build.CTRL, out / 'build', out / 'reuse', fw_gtest.Build(jobs=8))
    failed = False
    for suite, selected in [('srp_mbx.cpp', 'SrpTalkerKinds.*:*HeldRegistrations*'),
                            ('test_acmp_mbx.cpp', 'SrpFeedback.*')]:
        result = srp_arms.arm_srp(tree, repo / 'third_party/lwSRP', interfaces, test=(suite, selected))
        stem = f'spot-if{interfaces}-{suite}'
        (packet / (stem + '.log')).write_text(result.log)
        (packet / (stem + '.rc')).write_text(str(result.rc) + '\n')
        print(stem, 'rc', result.rc, flush=True)
        failed |= bool(result.rc)
    return failed

with ThreadPoolExecutor(max_workers=2) as workers:
    results = list(workers.map(run, [1, 2]))
raise SystemExit(int(any(results)))
