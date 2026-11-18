#!/usr/bin/env python3
"""Run new sink tests against the base's unchanged platform orchestration.

The new CSR helpers remain linked to satisfy the new test-facing API, but the
base platform never calls them. No production file in the checkout is changed.
Usage: python3 probe_old_platform.py REPOSITORY PACKET --jobs 8
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
p = argparse.ArgumentParser()
p.add_argument('repository', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--jobs', type=int, default=8)
a = p.parse_args()
root, packet = a.repository.resolve(), a.packet.resolve()
sys.path.insert(0, str(root/'sw/firmware/ctrl/test'))
import ctrl_build as cb
import plat_arms as pa
import fw_gtest
work = packet/'scratch/old-platform'
src = work/'ctrl'
if src.exists():
    shutil.rmtree(src)
shutil.copytree(cb.CTRL, src, ignore=shutil.ignore_patterns('__pycache__'))
(src/'plat/ctrl_plat.c').write_bytes(subprocess.check_output(
    ['git','show','cb96336d:sw/firmware/ctrl/plat/ctrl_plat.c'],cwd=root))
tree=cb.Tree(src,work/'build',work/'reuse',fw_gtest.Build(jobs=a.jobs))
r=pa.arm_platsinks(tree,*pa.SINK_SHAPES[0])
print(r.log)
sys.exit(r.rc)
