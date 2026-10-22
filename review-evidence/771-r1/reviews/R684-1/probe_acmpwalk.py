#!/usr/bin/env python3
"""Run only acmpwalk, plus a historical-model attribution control."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_arms
import ctrl_build
import ctrl_reuse
import fw_gtest

print('stack pin', ctrl_build.stack_pin())
print('processor pin', ctrl_reuse.prove_pin('tb/acmp_listener/sim_main.cpp'))
old_pin = '2cbed0a987c1e68402658d69459ab7e5aa571adc'
outcomes = {}

def run(name):
    out = packet / 'scratch' / name
    reuse = out / 'reuse'
    ctrl_reuse.cut_reuse(reuse)
    if name == 'acmpwalk-old-model':
        # Change only the disposable extracted listener oracle. No repository mutation.
        path = 'tb/acmp_listener/sim_main.cpp'
        source = subprocess.check_output(['git', '-C', str(root / 'protocol-processor'),
                                          'show', old_pin + ':' + path]).decode()
        spec = next(s for n, p, s in ctrl_reuse.REUSE if n == 'pp_acmp_reuse.inc')
        lines = []
        for what, first, end, inclusive in spec:
            lines += ctrl_reuse.cut(source.splitlines(), what, first, end, inclusive)
        (reuse / 'pp_acmp_reuse.inc').write_text('\n'.join(lines) + '\n')
    tree = ctrl_build.Tree(ctrl_build.CTRL, out / 'build', reuse, fw_gtest.Build(jobs=4))
    result = ctrl_arms.arm_acmpwalk(tree)
    raw = result.log
    (out / 'raw.log').write_text(raw)
    (packet / (name + '.raw.log')).write_text(raw)
    public = raw.replace(str(root), '<repo>').replace(str(packet), '<packet>')
    (packet / (name + '.log')).write_text(public)
    (packet / (name + '.rc')).write_text(str(result.rc) + '\n')
    return name, {'rc': result.rc, 'raw_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                  'reuse_sha256': hashlib.sha256((reuse / 'pp_acmp_reuse.inc').read_bytes()).hexdigest()}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    outcomes = dict(pool.map(run, ['acmpwalk-adopted', 'acmpwalk-old-model']))
(packet / 'acmpwalk-results.json').write_text(json.dumps(outcomes, indent=2) + '\n')
print(json.dumps(outcomes, indent=2))
assert outcomes['acmpwalk-adopted']['rc'] == 1
assert outcomes['acmpwalk-old-model']['rc'] == 0
