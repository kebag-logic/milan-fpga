#!/usr/bin/env python3
"""Focused review probes; usage: probe.py CHECKOUT PACKET. No checkout edits."""
import concurrent.futures
import os
from pathlib import Path
import shutil
import subprocess
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
scratch = packet / 'scratch'
os.environ['TMPDIR'] = str(scratch)
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import ctrl_build as b
import plat_arms as p
import ctrl_mutants as m
import sink_mutants as s

def run(name):
    root = scratch / name
    root.mkdir(parents=True, exist_ok=True)
    src = b.CTRL
    stack = b.STACK
    plant = None
    if name == 'old-platform':
        src = root / 'ctrl'
        shutil.copytree(b.CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
        (src / 'plat/ctrl_plat.c').write_bytes(subprocess.check_output(
            ['git', '-C', str(repo), 'show', '66c6edf3:sw/firmware/ctrl/plat/ctrl_plat.c']))
    elif name.startswith('sink-'):
        plant = next(x for x in s.mutants(m.Mutant) if x.name == name)
        src, stack = m.plant(plant, root)
    tree = b.Tree(src, root / 'build', root / 'reuse', b.fw_gtest.Build(jobs=4), stack)
    outcomes = [p.arm_platsinks(tree, *p.SINK_SHAPES[0])]
    if name == 'clean':
        outcomes.append(p.arm_platsinks(tree, *p.SINK_SHAPES[1]))
    log = '\n'.join(x.log for x in outcomes)
    for path, replacement in [(str(repo), '<checkout>'), (str(packet), '<packet>')]:
        log = log.replace(path, replacement)
    (packet / (name + '.log')).write_text(log + '\n')
    if plant:
        ok = all(m.caught(test, needle, outcomes[0]) for arm, test, needle in plant.kills())
    elif name == 'old-platform':
        failed = b.fw_gtest.failed_tests(log)
        ok = outcomes[0].rc == 1 and all(x in failed for x in [s.S4, s.S5, s.S6, s.S7, s.S10])
    else:
        ok = all(x.rc == 0 for x in outcomes)
    (packet / (name + '.rc')).write_text(' '.join(str(x.rc) for x in outcomes) + '\n')
    return name, ok

names = ['clean', 'old-platform', 'sink-every-pass-rewrites', 'sink-redo-refusal-skipped']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, names))
for name, ok in results:
    print(name, 'EXPECTED RESULT' if ok else 'UNEXPECTED RESULT')
sys.exit(0 if all(ok for _, ok in results) else 1)
