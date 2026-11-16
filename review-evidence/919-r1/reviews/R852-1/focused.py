#!/usr/bin/env python3
"""Focused independent review execution; run from the reviewed checkout."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
PACKET = Path(__file__).resolve().parent
SCRATCH = PACKET / 'scratch'
SCRATCH.mkdir(exist_ok=True)
os.environ['TMPDIR'] = str(SCRATCH)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl/test'))
from ctrl_build import Tree, CTRL
import fw_gtest
import plat_arms

def platform(n):
    out = SCRATCH / f'platform-{n}'
    out.mkdir(exist_ok=True)
    tree = Tree(CTRL, out, out / 'reuse', fw_gtest.Build(jobs=6))
    result = plat_arms.arm_platboot(tree, n)
    (PACKET / f'platform-{n}.log').write_text(result.log)
    (PACKET / f'platform-{n}.rc').write_text(str(result.rc) + '\n')
    return f'platform-{n}', result.rc

def maps():
    out = SCRATCH / 'maps'
    out.mkdir(exist_ok=True)
    result = plat_arms.arm_platmap(Tree(CTRL, out, out / 'reuse', fw_gtest.Build(jobs=1)))
    (PACKET / 'maps.log').write_text(result.log)
    (PACKET / 'maps.rc').write_text(str(result.rc) + '\n')
    return 'maps', result.rc

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(platform, 1), pool.submit(platform, 2), pool.submit(maps)]
    results = [f.result() for f in futures]
for name, rc in results:
    print(f'{name}: rc {rc}', flush=True)
sys.exit(int(any(rc for _, rc in results)))
