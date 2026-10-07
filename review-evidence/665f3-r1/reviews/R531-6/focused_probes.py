#!/usr/bin/env python3
"""Independently grade round-7 controls and keep each complete arm log."""
import argparse
import json
from pathlib import Path
import sys

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
ap.add_argument('packet', type=Path)
ap.add_argument('--jobs', type=int, default=2)
a = ap.parse_args()
sys.path.insert(0, str(a.root / 'sw/firmware/ctrl/test'))
import ctrl_arms
import ctrl_mutants
import fw_gtest
from ctrl_build import CTRL, Tree
from ctrl_reuse import cut_reuse

out = a.packet / 'scratch/focused'
cut_reuse(out / 'reuse')
build = fw_gtest.Build(jobs=a.jobs)
arms = {'acmp': ctrl_arms.arm_acmp, 'acmpif2': ctrl_arms.arm_acmpif2}
summary = []
for name, arm in arms.items():
    result = arm(Tree(CTRL, out / 'control', out / 'reuse', build))
    (a.packet / f'focused-control-{name}.log').write_text(result.log)
    assert result.rc == 0, name
    summary.append({'control': name, 'rc': result.rc})

names = ('app-maap-mac-per-interface', 'app-own-mac-per-interface',
         'app-three-way-bound-drops-maap', 'app-three-way-bound-one-maap-poll')
for name in names:
    m, = [m for m in ctrl_mutants.MUTANTS if m.name == name]
    tree = Tree(ctrl_mutants.plant(m, out / 'mutants'), out / name, out / 'reuse', build)
    # Run both shapes, including controls where the defect only affects IF1.
    for arm_name, arm in arms.items():
        result = arm(tree)
        (a.packet / f'focused-{name}-{arm_name}.log').write_text(result.log)
        failures = [line.strip() for line in result.log.splitlines() if '[FAIL]' in line]
        expected = [kill for kill in m.kills() if kill[0] == arm_name]
        if expected:
            _, test, needle = expected[0]
            assert result.rc == 1 and len(failures) == 1, (name, arm_name, result.rc, failures)
            assert ctrl_mutants.names(failures[0], test, needle), (name, arm_name, failures)
        else:
            assert result.rc == 0 and not failures, (name, arm_name, failures)
        summary.append({'mutant': name, 'arm': arm_name, 'rc': result.rc, 'failures': failures,
                        'expected': 'one named failure' if expected else 'unchanged control passes'})
print(json.dumps(summary, indent=2))
