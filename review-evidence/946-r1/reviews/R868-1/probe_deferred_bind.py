#!/usr/bin/env python3
"""Build the unchanged platform with one additional ordering test.

Usage: python3 probe_deferred_bind.py REPOSITORY PACKET --jobs 8
An exit of 1 with the named assertion is the reproduced defect.
"""
import argparse
from pathlib import Path
import shutil
import sys
p = argparse.ArgumentParser()
p.add_argument('repository', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=8)
a = p.parse_args()
root, packet = a.repository.resolve(), a.packet.resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build as cb
import plat_arms as pa
import fw_gtest
work = packet / 'scratch/deferred-bind'
tests = work / 'tests'
tests.mkdir(parents=True, exist_ok=True)
original = (pa.HERE / 'test_plat_sinks.cpp').read_text()
original = original.replace('namespace {', 'namespace {\nvoid observe_bound_format();', 1)
hook = 'extern "C" std::uint32_t mbx_hal_read32(std::uint32_t offset) {'
assert original.count(hook) == 1
original = original.replace(hook, hook + '\n    observe_bound_format();')
marker = '}  // namespace'
pos = original.rfind(marker)
assert pos >= 0
(tests / 'test_plat_sinks.cpp').write_text(original[:pos] + (packet / 'deferred_bind.cpp').read_text() + '\n' + original[pos:])
shutil.copyfile(pa.HERE / 'plat_bus.cpp', tests / 'plat_bus.cpp')
pa.HERE = tests
tree = cb.Tree(cb.CTRL, work / 'build', work / 'reuse', fw_gtest.Build(jobs=a.jobs))
r = pa.arm_platsinks(tree, *pa.SINK_SHAPES[0])
print(r.log)
sys.exit(r.rc)
