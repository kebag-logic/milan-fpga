#!/usr/bin/env python3
"""Run the extra retry probe without modifying any checkout source."""
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path.cwd()
packet = Path(__file__).resolve().parent
control = '--control' in sys.argv
name = 'retry-control' if control else 'retry-probe'
out = packet / 'scratch' / name
out.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
from ctrl_build import Tree, CTRL
import fw_gtest
import plat_arms
original = fw_gtest.compile_tests
def with_probe(build, inc, sources, *args, **kwargs):
    sources = [packet / 'retry_probe.cpp' if p.name == 'test_plat_phy.cpp' else p for p in sources]
    if control:
        inc = [*inc, '-DREVIEW_NO_WRITE_FAULT']
    return original(build, inc, sources, *args, **kwargs)
fw_gtest.compile_tests = with_probe
r = plat_arms.arm_platboot(Tree(CTRL, out, out / 'reuse', fw_gtest.Build(jobs=8)), 1)
(packet / f'{name}.log').write_text(r.log)
(packet / f'{name}.rc').write_text(str(r.rc) + '\n')
print(r.log)
sys.exit(r.rc)
