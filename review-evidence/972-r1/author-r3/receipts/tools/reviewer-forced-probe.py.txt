#!/usr/bin/env python3
"""Reproduce focused source-head checks. All builds and copies stay under packet/scratch.
Usage: python3 focused.py CHECKOUT PACKET TASK --jobs 2
Tasks: adp, plat1, plat2, adp-plants, phy-plants, forced-head, forced-base.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('checkout', type=Path)
ap.add_argument('packet', type=Path)
ap.add_argument('task')
ap.add_argument('--jobs', type=int, default=2)
a = ap.parse_args()
root = a.checkout.resolve()
out = a.packet.resolve() / 'scratch' / a.task
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build as b
import ctrl_arms
import plat_arms
import ctrl_mutants
import adp_first_mutants
import fw_gtest

build = fw_gtest.Build(jobs=a.jobs)
tree = b.Tree(b.CTRL, out / 'build', out / 'reuse', build)
if a.task in ('adp', 'plat1', 'plat2'):
    result = (ctrl_arms.arm_adp(tree) if a.task == 'adp' else
              plat_arms.arm_platboot(tree, int(a.task[-1])))
    print(result.log)
    sys.exit(result.rc)
if a.task.endswith('-plants'):
    from ctrl_reuse import cut_reuse
    cut_reuse(tree.reuse)
    names = {'plat-phy-boot-restarts-whatever-held', 'plat-phy-arm-publishes-nothing',
             'plat-phy-outcome-unchecked'}
    table = (adp_first_mutants.MUTANTS if a.task == 'adp-plants' else
             [m for m in ctrl_mutants.MUTANTS if m.name in names])
    escaped = 0
    for m in table:
        src, stack = ctrl_mutants.plant(m, out / m.name)
        candidate = b.Tree(src, out / m.name / 'build', out / 'reuse', build, stack)
        results = {}
        for arm, test, needle in m.kills():
            if arm not in results:
                results[arm] = (plat_arms.arm_platboot(candidate, 1) if arm == 'platboot1' else
                                ctrl_arms.arm_walk(candidate) if arm == 'walk' else
                                ctrl_arms.arm_adp(candidate))
                print(f'=== {m.name} / {arm} ===\n{results[arm].log}', flush=True)
            caught = ctrl_mutants.caught(test, needle, results[arm])
            print(f'KILL {m.name} {test}: {caught}', flush=True)
            escaped += not caught
    print(f'PLANTS {len(table)}; missed named kills {escaped}')
    sys.exit(bool(escaped))
if a.task.startswith('forced-'):
    # Add an independent scenario to a disposable copy of the existing PHY fixture.
    # The PHY is gigabit-capable; its advertisement is already correct, but
    # BMCR forces 100 Mb/s. The old boot normalized BMCR; the new skip must
    # not publish that unsupported mode merely because registers 4/9 match.
    tests = out / 'tests'
    shutil.copytree(b.HERE, tests, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
    test = tests / 'test_plat_phy.cpp'
    extra = '''
TEST_F(PlatPhy, ReviewHeldAdvertisementForced100) {
    peer.gigabit(7u);
    peer.regs[4] = 0x0001u;
    peer.regs[9] = 0x0200u;
    peer.regs[0] = 0x2100u; // AN disabled, forced 100 Mb/s full duplex
    peer.regs[1] &= ~0x0020u; // no completed autonegotiation
    arm_again();
    (void)poll(now);
    next();
    std::printf("PROBE BMCR=0x%04x publication=%u restarts=%u renegotiations=%u\\n",
                peer.regs[0], peer.word, peer.restarts, phy.renegotiations);
    EXPECT_TRUE((peer.regs[0] & 0x1000u) != 0u) << "boot must enable autonegotiation";
    EXPECT_NE(peer.word, kFull100) << "boot must not publish forced 100 Mb/s";
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}
'''
    text = test.read_text()
    assert text.endswith('}  // namespace\n')
    test.write_text(text[:-len('}  // namespace\n')] + extra + '\n}  // namespace\n')
    plat_arms.HERE = tests
    if a.task == 'forced-base':
        src = out / 'ctrl'
        shutil.copytree(b.CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
        (src / 'plat/ctrl_plat_phy.c').write_bytes(subprocess.check_output(
            ['git', '-C', str(root), 'show', 'dd163e41:sw/firmware/ctrl/plat/ctrl_plat_phy.c']))
        tree = b.Tree(src, out / 'build', out / 'reuse', build)
    fw_gtest.EXECUTION.run = False
    plat_arms.arm_platboot(tree, 1)
    exe = tree.out / 'test_plat_boot_if1'
    r = subprocess.run([str(exe), '--gtest_filter=PlatPhy.ReviewHeldAdvertisementForced100'])
    sys.exit(r.returncode)
raise SystemExit('unknown task')
