#!/usr/bin/env python3
"""Focused baseline and two regression mutations; all build products stay in packet scratch."""
import json
import shutil
import sys
from pathlib import Path

tree, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
sys.path[:0] = [str(tree / 'sw/firmware/ctrl/test'), str(tree / 'sw/firmware/gtest')]
import aecp_mutants as m
import aecp_arms
import fw_gtest
from ctrl_build import Tree

out = packet / 'scratch/mutations'
out.mkdir(parents=True, exist_ok=True)
m.controls()
print('PASS full table diagnostic controls', flush=True)
print('Stack pin:', m.stack_pin(m.STACK.resolve()), flush=True)
config = tree / 'configs/endstation_ax7101_1x1_tdm8.yaml'
selected = ('reboot-retries-after-its-success', 'owed-round-beside-the-queue')
defs = tuple(d for d in m.DEFECTS if d.name in selected)
assert len(defs) == 2
tests = ':'.join(test for d in defs for test, _ in d.checks)
baseline = Tree(m.CTRL, out / 'baseline/build', out / 'baseline/reuse', fw_gtest.Build(jobs=8), m.STACK)
result = aecp_arms.core_arm(baseline, config, 2, 'app', tests)
(packet / 'mutation-baseline.log').write_text(result.log)
print('Baseline result:', result, flush=True) if result.rc != 0 else print('PASS selected baseline', flush=True)
assert result.rc == 0
m.DEFECTS = defs
m.controls = lambda: None
escaped = m.campaign(out / 'planted', jobs=8, stack=m.STACK)
for name in selected:
    shutil.copyfile(out / 'planted' / (name + '.log'), packet / (name + '.log'))
shutil.copyfile(out / 'planted/results.json', packet / 'mutation-results.json')
print('RESULT:', 'FAIL' if escaped else 'PASS two mutations caught on named checks', flush=True)
raise SystemExit(int(escaped))
