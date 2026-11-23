#!/usr/bin/env python3
"""Run focused tests without editing tracked source. Usage: run_focused.py CHECKOUT PACKET."""
import concurrent.futures
import json
from pathlib import Path
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
sys.dont_write_bytecode = True
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import fw_gtest
import srp_arms
from ctrl_build import Tree, CTRL

scratch = packet / 'scratch'
tests = scratch / 'tests'
tests.mkdir(parents=True, exist_ok=True)
suite = root / 'sw/firmware/ctrl/test/srp_link_pass.cpp'
# A private test-directory copy leaves both the checkout and its index untouched.
for source in suite.parent.iterdir():
    if source.is_file() and source.suffix in ('.hpp', '.h'):
        (tests / source.name).write_bytes(source.read_bytes())
combined = tests / 'probe_stale_mark.cpp'
combined.write_bytes(suite.read_bytes() + (packet / 'probe_stale_mark.cpp').read_bytes())
srp_arms.HERE = tests

def run(stem):
    out = scratch / ('probe-' + stem)
    tree = Tree(CTRL, out, out / 'reuse', fw_gtest.Build(jobs=8))
    result = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', 1,
                            test=combined.name, config=root / 'configs' / (stem + '.yaml'))
    log = result.log.replace(str(root), '<checkout>').replace(str(packet), '<packet>')
    (packet / (stem + '.log')).write_text(log)
    (packet / (stem + '.rc')).write_text(str(result.rc) + '\n')
    return {'shape': stem, 'rc': result.rc, 'arm': result.arm}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, ['endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8']))
print(json.dumps(results, indent=2))
sys.exit(int(any(r['rc'] for r in results)))
