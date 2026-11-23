#!/usr/bin/env python3
"""Run both published regression probes and current early tests: CHECKOUT PACKET.
Four concurrent arms with four compiler jobs each; all builds remain in scratch.
"""
import concurrent.futures as cf
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import traceback
root, packet = (Path(x).resolve() for x in sys.argv[1:3])
scratch = packet / 'scratch/probes'
scratch.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(scratch)
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build as cb
import fw_gtest
import srp_arms
old = scratch / 'old-src'
shutil.copytree(cb.CTRL, old, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
for name in ('srp_mbx.c', 'srp_mbx.h'):
    (old / 'srp' / name).write_bytes(subprocess.check_output(['git', '-C', str(root), 'show', 'f863258d:sw/firmware/ctrl/srp/' + name]))
test = scratch / 'combined.cpp'
test.write_text((packet / 'probes.cpp').read_text().replace('#include "srp_mbx.cpp"', '#include "' + str(cb.HERE / 'srp_mbx.cpp') + '"') + '\nnamespace {\n' + (packet / 'stale_count_probe.cpp').read_text() + '\n}\n')
def one(spec):
    version, shape, interfaces = spec
    name = f'probe-{version}-{shape}-if{interfaces}'
    out = scratch / name
    out.mkdir(exist_ok=True)
    tree = cb.Tree(old if version == 'old' else cb.CTRL, out, out / 'reuse', fw_gtest.Build(jobs=4))
    try:
        result = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', interfaces,
            test=(str(test), 'SrpEarlyTalker.*:SrpStaleCountProbe.*'),
            config=srp_arms.DEFAULT_ENTITY if shape == '1x1' else srp_arms.ENTITY_8X8)
        rc, log = result.rc, result.log
    except Exception:
        rc, log = 2, traceback.format_exc()
    for source, replacement in ((str(root), '<checkout>'), (str(packet), '<packet>')):
        log = log.replace(source, replacement)
    (packet / (name + '.log')).write_text(log)
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, rc, flush=True)
    return dict(name=name, rc=rc, expected=1 if version == 'old' else 0)
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(one, [(v,s,i) for v in ('head','old') for s in ('1x1','8x8') for i in (1,2)]))
(packet / 'probe-results.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(r['rc'] != r['expected'] for r in results))
