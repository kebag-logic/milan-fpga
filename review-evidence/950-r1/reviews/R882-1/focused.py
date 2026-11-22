#!/usr/bin/env python3
"""Focused exact-head review probes. Usage: focused.py CHECKOUT PACKET MODE.

All altered source and builds remain in PACKET/scratch. Four workers, each
with at most four compiler jobs, are run by run_review.py.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
mode = sys.argv[3]
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
from ctrl_build import CTRL, STACK, Tree, stack_pin
import aecp_arms
import aecp_mutants as am
import ctrl_mutants as cm
import fw_gtest
import plat_arms

work = packet / 'scratch' / mode
work.mkdir(parents=True, exist_ok=True)
receipts = packet / 'receipts' / mode
receipts.mkdir(parents=True, exist_ok=True)
print('stack pin:', stack_pin(STACK), flush=True)
build = fw_gtest.Build(jobs=4)
status = 0

def record(name, result, expected=0):
    global status
    (receipts / (name + '.log')).write_text(result.log)
    print(name, 'rc', result.rc, 'expected', expected, flush=True)
    status |= result.rc != expected

if mode in ('head', 'base'):
    src = CTRL
    if mode == 'base':
        src = work / 'ctrl'
        shutil.copytree(CTRL, src, dirs_exist_ok=True)
        shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True)
        for path in ('aecp/aecp.c', 'aecp/aecp_commands.c', 'plat/ctrl_plat.c'):
            data = subprocess.check_output(['git', '-C', str(repo), 'show', '15168e14:sw/firmware/ctrl/' + path])
            (src / path).write_bytes(data)
    tree = Tree(src, work / 'build', work / 'reuse', build, STACK)
    for config, count in plat_arms.SINK_SHAPES:
        record(config.stem + '-platform', plat_arms.arm_platsinks(tree, config, count), int(mode == 'base'))
        selected = ('*' if mode == 'head' and count == 0 else
                    'Core.AWaitingFormatChangeMakesItsRunningCheckAgainOnceApplied')
        record(config.stem + '-core', aecp_arms.core_arm(tree, config, 2, 'app', selected), int(mode == 'base'))
elif mode == 'aecp-plants':
    am.controls()
    print('full AECP table controls passed before selecting rows', flush=True)
    am.controls = lambda: None
    names = {r[0] for r in am.aecp_again_mutants.ROWS} | {
        'waiting-change-not-redone', 'waiting-success-not-notified', 'waiting-failure-notified',
        'waiting-failure-not-republished', 'waiting-failure-reports-the-request'}
    am.DEFECTS = tuple(d for d in am.DEFECTS if d.name in names)
    assert len(am.DEFECTS) == 12
    status = am.campaign(work, jobs=4)
    for p in work.glob('*.log'):
        shutil.copyfile(p, receipts / p.name)
    shutil.copyfile(work / 'results.json', receipts / 'results.json')
elif mode == 'control-plants':
    names = {'again-unchecked-onto-a-stream', 'again-of-stream-zero', 'asking-failed-unreported',
             'asking-failed-any-listener', 'asking-failed-without-a-listener', 'asking-failed-of-output-zero'}
    rows = [m for m in cm.MUTANTS if m.name in names]
    assert len(rows) == 6
    summary = []
    arms = {'platsinks8': plat_arms.SINK_SHAPES[0], 'platsinks1': plat_arms.SINK_SHAPES[1]}
    for m in rows:
        src, stack = cm.plant(m, work)
        tree = Tree(src, work / 'build', work / 'reuse', build, stack)
        for i, (arm, test, needle) in enumerate(m.kills()):
            result = plat_arms.arm_platsinks(tree, *arms[arm])
            killed = cm.caught(test, needle, result)
            (receipts / f'{m.name}-{i}.log').write_text(result.log)
            summary.append(dict(name=m.name, arm=arm, test=test, needle=needle, caught=killed))
            print(m.name, arm, 'caught', killed, flush=True)
            status |= not killed
    (receipts / 'results.json').write_text(json.dumps(summary, indent=2) + '\n')
else:
    raise ValueError(mode)
raise SystemExit(int(bool(status)))
