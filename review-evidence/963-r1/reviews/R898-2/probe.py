#!/usr/bin/env python3
"""probe.py REPO OUT LABEL [--plant PATH OLD NEW]... [--want caught|escaped|pass] [--words W]
[--arm app|work] [--tests T]

In an isolated copy of REPO's sw/firmware/ctrl (and ctrl_nvm) under OUT, apply each plant (OLD must occur exactly once in PATH, relative to ctrl/), then build and run the AECP core arm
the campaign uses (aecp_arms.core_arm, 1x1 config) on the selected tests. The arm compiles REPO's own
test/test_aecp.cpp (aecp_arms uses its own directory), so a different test is probed by pointing REPO at a copy. Grades with the campaign's own caught():
  --want pass     the run exits 0
  --want caught   every selected test fails and its failure text contains WORDS
  --want escaped  the run exits 0 (the plant is not detected)
Writes OUT/LABEL.log and prints one verdict line. Exit 0 when the observed outcome is the wanted one."""
import argparse
import shutil
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('repo', type=Path)
ap.add_argument('out', type=Path)
ap.add_argument('label')
ap.add_argument('--plant', nargs=3, action='append', default=[])
ap.add_argument('--want', choices=('pass', 'caught', 'escaped'), required=True)
ap.add_argument('--words', default='')
ap.add_argument('--arm', default='app')
ap.add_argument('--tests', default='Core.MapEditsAreTheirDefinitionRowForRow')
ap.add_argument('--jobs', type=int, default=3)
a = ap.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str((a.repo / 'sw/firmware/ctrl/test').resolve()))
import aecp_arms  # noqa: E402
import aecp_mutants as m  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Tree  # noqa: E402

out = a.out.resolve() / a.label
if out.exists():
    shutil.rmtree(out)
src = out / 'work/ctrl'
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
for path, old, new in a.plant:
    t = src / path
    text = t.read_text()
    assert text.count(old) == 1, (path, old, text.count(old))
    t.write_text(text.replace(old, new))
tree = Tree(src, out / 'work/build', out / 'work/reuse', fw_gtest.Build(jobs=a.jobs), STACK)
config = ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
result = aecp_arms.core_arm(tree, config, 1 if a.arm == 'work' else 2, a.arm, a.tests)
(a.out.resolve() / f'{a.label}.log').write_text(result.log)
tests = a.tests.split(':')
if a.want == 'caught':
    got = all(m.caught(t, a.words, result) for t in tests)
else:
    got = result.rc == 0
print(f"[{'as-wanted' if got else 'NOT-as-wanted'}] {a.label}: want {a.want}, rc {result.rc}, tests {a.tests}", flush=True)
sys.exit(0 if got else 1)
