#!/usr/bin/env python3
"""Run the scoped platform arms and all 19 context-format plants.

Usage: python3 focused_firmware.py REPOSITORY PACKET --jobs 8
All generated sources and objects stay in PACKET/scratch.
"""
import argparse
from pathlib import Path
import sys

p = argparse.ArgumentParser()
p.add_argument('repository', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=8)
a = p.parse_args()
root, packet = a.repository.resolve(), a.packet.resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build as cb
import ctrl_mutants as cm
import plat_arms as pa
import sink_mutants as sm
import fw_gtest

scratch = packet / 'scratch/firmware'
scratch.mkdir(parents=True, exist_ok=True)
build = fw_gtest.Build(jobs=a.jobs)
tree = cb.Tree(cb.CTRL, scratch / 'clean', scratch / 'reuse', build)
failures = 0
for label, arm in [('plat', pa.arm_plat),
                   ('sinks8', lambda t: pa.arm_platsinks(t, *pa.SINK_SHAPES[0])),
                   ('sinks1', lambda t: pa.arm_platsinks(t, *pa.SINK_SHAPES[1]))]:
    result = arm(tree)
    (packet / ('firmware-' + label + '.log')).write_text(result.log)
    print(f'{label}: rc={result.rc}', flush=True)
    failures += result.rc != 0
for m in sm.mutants(cm.Mutant):
    src, stack = cm.plant(m, scratch / 'mutants')
    tree = cb.Tree(src, scratch / 'mutants/work/build', scratch / 'reuse', build, stack)
    logs, caught = [], True
    for arm, test, needle in m.kills():
        result = pa.arm_plat(tree) if arm == 'plat' else pa.arm_platsinks(tree, *pa.SINK_SHAPES[0])
        ok = cm.caught(test, needle, result)
        caught &= ok
        logs.append(f'EXPECTED: {test}: {needle}\nRC: {result.rc}; named catch: {ok}\n{result.log}')
    (packet / ('plant-' + m.name + '.log')).write_text('\n'.join(logs))
    print(f'{m.name}: {"CAUGHT" if caught else "ESCAPED"}', flush=True)
    failures += not caught
print(f'focused firmware failures: {failures}', flush=True)
sys.exit(bool(failures))
