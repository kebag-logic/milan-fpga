#!/usr/bin/env python3
"""Reproduce the scoped review suites; all disposable files stay in scratch.

Usage: python3 run_focused.py CHECKOUT PACKET
Runs four independent builds concurrently, each with four compiler jobs.
The base arm uses the published base adapter and current regression tests.
"""
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys
import traceback

root, packet = (Path(x).resolve() for x in sys.argv[1:3])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build as cb
import srp_arms
import plat_arms
import fw_gtest

scratch = packet / 'scratch/focused'
scratch.mkdir(parents=True, exist_ok=True)
base = scratch / 'base-src'
if not base.exists():
    shutil.copytree(cb.CTRL, base, ignore=shutil.ignore_patterns('__pycache__'))
for name in ('srp_mbx.c', 'srp_mbx.h'):
    data = subprocess.check_output(['git', '-C', str(root), 'show', f'dd163e41:sw/firmware/ctrl/srp/{name}'])
    (base / 'srp' / name).write_bytes(data)

def one(spec):
    version, shape, suite = spec
    name = f'{version}-{shape}-{suite}'
    dest = scratch / name
    dest.mkdir(exist_ok=True)
    tree = cb.Tree(base if version == 'base' else cb.CTRL, dest, dest / 'reuse', fw_gtest.Build(jobs=4))
    cfg = srp_arms.DEFAULT_ENTITY if shape == '1x1' else srp_arms.ENTITY_8X8
    try:
        if suite == 'platsinks':
            outcome = plat_arms.arm_platsinks(tree, cfg, 0 if shape == '1x1' else 7)
        else:
            selected = 'SrpEarlyTalker.*:SrpTalkerKinds.*' if version == 'base' else '*'
            outcome = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', 1,
                                       test=(suite + '.cpp', selected), config=cfg)
        log, rc = outcome.log, outcome.rc
    except Exception:
        log, rc = traceback.format_exc(), 2
    (packet / (name + '.log')).write_text(log)
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    result = {'name': name, 'rc': rc}
    print(json.dumps(result), flush=True)
    return result

specs = [(v, s, t) for v in ('head', 'base') for s in ('1x1', '8x8')
         for t in ('srp_mbx', 'platsinks')]
specs += [('head', s, 'srp_listeners') for s in ('1x1', '8x8')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(one, specs))
(packet / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(r['rc'] != (1 if r['name'].startswith('base-') else 0) for r in results))
