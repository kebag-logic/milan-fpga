#!/usr/bin/env python3
"""Run the published re-attach probe and the delta control at both shipping shapes."""
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
sys.dont_write_bytecode = True
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import fw_gtest
import srp_arms
from ctrl_build import Tree, CTRL

tests = packet / 'scratch/tests'
source = tests / 'probe_reattach_elided.cpp'
source.write_bytes((packet / source.name).read_bytes())
srp_arms.HERE = tests
prior = packet / 'scratch/prior-ctrl'
shutil.copytree(CTRL, prior, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
for name in ['srp_mbx.c', 'srp_mbx.h']:
    data = subprocess.check_output(['git', '-C', str(root), 'show', '9a71daa9:sw/firmware/ctrl/srp/' + name])
    (prior / 'srp' / name).write_bytes(data)

def run(spec):
    mode, stem = spec
    out = packet / 'scratch' / (mode + '-' + stem)
    firmware = prior if mode == 'prior-stale-mark' else CTRL
    tree = Tree(firmware, out, out / 'reuse', fw_gtest.Build(jobs=4))
    test = ('probe_stale_mark.cpp', 'SrpLinkPass.AnElidedUpDoesNotAuthorizeAFreshUpInsideAPass') if mode == 'prior-stale-mark' else 'probe_reattach_elided.cpp'
    result = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', 1, test=test,
                            config=root / 'configs' / (stem + '.yaml'))
    log = result.log.replace(str(root), '<checkout>').replace(str(packet), '<packet>')
    (packet / (mode + '-' + stem + '.log')).write_text(log)
    (packet / (mode + '-' + stem + '.rc')).write_text(str(result.rc) + '\n')
    return {'mode': mode, 'shape': stem, 'rc': result.rc}

specs = [(mode, stem) for mode in ['prior-stale-mark', 'reattach']
         for stem in ['endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8']]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, specs))
print(json.dumps(results, indent=2))
sys.exit(int(any(r['rc'] for r in results)))
