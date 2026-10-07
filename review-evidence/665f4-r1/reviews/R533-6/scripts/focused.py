#!/usr/bin/env python3
"""Focused exact-source suites and scratch-only recovery fault control."""
import argparse
import json
import shutil
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('--mode', choices=['suites', 'campaign', 'probes'], required=True)
p.add_argument('--jobs', type=int, default=4)
a = p.parse_args()
repo = a.repo.resolve()
packet = Path(__file__).resolve().parents[1]
scratch = packet / 'scratch' / a.mode
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import srp_arms, srp_mutants, ctrl_arms, fw_gtest
from ctrl_build import CTRL, Tree
lw = repo / 'third_party/lwSRP'
ctrl_arms.lwsrp_pin(lw)
build = fw_gtest.Build(jobs=a.jobs)
failed = False
if a.mode == 'campaign':
    failed = srp_mutants.campaign(scratch, lw, jobs=a.jobs)
    dest = packet / 'receipts/campaign'
    dest.mkdir(exist_ok=True)
    for f in scratch.glob('*.log'):
        shutil.copyfile(f, dest / f.name)
    sys.exit(int(failed))
if a.mode == 'suites':
    tree = Tree(CTRL, scratch / 'build', scratch / 'reuse', build)
    for n in (1, 2):
        for suite in ('srp_mbx.cpp', 'srp_rx_retry.cpp', 'srp_app.cpp', 'srp_walk.cpp', 'srp_latency.cpp'):
            r = srp_arms.arm_srp(tree, lw, n, test=suite)
            print(r.arm, r.rc, r.log, flush=True)
            failed |= bool(r.rc)
        r = srp_arms.arm_srp(tree, lw, n, debug=True)
        print(r.arm, r.rc, r.log, flush=True)
        failed |= bool(r.rc)
    for r in (ctrl_arms.arm_maap(tree), ctrl_arms.arm_maap_if2(tree)):
        print(r.arm, r.rc, r.log, flush=True)
        failed |= bool(r.rc)
    sys.exit(int(failed))

srp_arms.HERE = packet / 'scripts'
results = []
for mode in ('control', 'retry-removed'):
    src = CTRL
    if mode == 'retry-removed':
        src = scratch / 'mutated-ctrl'
        shutil.copytree(CTRL, src, dirs_exist_ok=True)
        f = src / 'srp/srp_mbx.c'
        before = 'if (apply_receive(m,&m->pending_rx))'
        data = f.read_text()
        assert data.count(before) == 1
        f.write_text(data.replace(before, 'if (false)'))
        (packet / 'receipts/retry-plant.json').write_text(json.dumps({
            'path': 'sw/firmware/ctrl/srp/srp_mbx.c', 'before': before, 'after': 'if (false)'
        }, indent=2) + '\n')
    for n in (1, 2):
        selected = 'Srp.Review*' if mode == 'control' else 'Srp.ReviewWithdrawDuringExhaustionSurvivesRecovery'
        r = srp_arms.arm_srp(Tree(src, scratch / mode / f'if{n}', scratch / 'reuse', build),
                             lw, n, test=('independent.cpp', selected))
        (packet / 'receipts' / f'{mode}-if{n}.log').write_text(r.log)
        print(mode, n, r.rc, r.log, flush=True)
        if mode == 'control':
            ok = r.rc == 0
        else:
            ok = r.rc != 0 and 'adapter.ifs[0].active[0]' in r.log and selected in fw_gtest.failed_tests(r.log)
        failed |= not ok
        results.append({'mode': mode, 'interfaces': n, 'test_rc': r.rc, 'expected_result_observed': ok})
(packet / 'receipts/probes.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(int(failed))
