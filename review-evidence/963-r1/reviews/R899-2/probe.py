#!/usr/bin/env python3
"""Focused order probe. Usage: python3 -B probe.py CHECKOUT PACKET."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

root, out = map(lambda x: Path(x).resolve(), sys.argv[1:])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_arms
import aecp_mutants as m
import fw_gtest
from ctrl_build import CTRL, STACK, Tree

scratch = out / 'scratch/probe'
src = scratch / 'ctrl'
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'), dirs_exist_ok=True)
tree = Tree(src, scratch / 'build', scratch / 'reuse', fw_gtest.Build(jobs=16), STACK)
test = src / 'test/test_aecp.cpp'
aecp_arms.HERE = src / 'test'  # core_arm otherwise compiles the original checkout's tests
production = src / 'aecp/aecp_maps.c'
head_test, head_prod = test.read_bytes(), production.read_bytes()
d = next(d for d in m.DEFECTS if d.name == 'map-read-before-legal')
results = {}
def run(label):
    r = aecp_arms.core_arm(tree, root / 'configs/endstation_ax7101_1x1_tdm8.yaml', 2,
                           'core', 'Core.MapEditsAreTheirDefinitionRowForRow:Core.MapEditWorkObservesEachOutputStreamOnce')
    log = r.log.replace(str(out), '<packet>').replace(str(root), '<review-clone>')
    (out / (label + '.log')).write_text(log)
    results[label] = {'rc': r.rc, 'caught_by_named_diagnostic': all(m.caught(t, w, r) for t,w in d.checks)}
    print(label, results[label], flush=True)
    return r

try:
    assert run('control').rc == 0
    assert production.read_text().count(d.old) == 1
    production.write_text(production.read_text().replace(d.old, d.new))
    run('order-plant')
    assert results['order-plant']['caught_by_named_diagnostic']
    test.write_bytes(subprocess.check_output(['git', '-C', str(root), 'show', '4cca9569:sw/firmware/ctrl/test/test_aecp.cpp']))
    assert run('old-test-order-plant').rc == 0
    production.write_bytes(head_prod)
    test.write_bytes(head_test.replace(b'EXPECT_GE(seen[name],20u)', b'EXPECT_GE(seen[name],1000000u)'))
    assert run('tally-probe').rc != 0
finally:
    test.write_bytes(head_test)
    production.write_bytes(head_prod)
    (out / 'probe-results.json').write_text(json.dumps(results, indent=2) + '\n')
