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

def run(stem):
    out = scratch / ('safety-' + stem)
    tree = Tree(CTRL, out, out / 'reuse', fw_gtest.Build(jobs=8))
    result = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', 1,
                            test=('srp_mbx.cpp', 'Srp.LinkLevelLossAndFirstDownEventAreFailClosed:Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive:Srp.ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord'), config=root / 'configs' / (stem + '.yaml'))
    log = result.log.replace(str(root), '<checkout>').replace(str(packet), '<packet>')
    (packet / ('safety-' + stem + '.log')).write_text(log)
    (packet / ('safety-' + stem + '.rc')).write_text(str(result.rc) + '\n')
    return {'shape': stem, 'rc': result.rc, 'arm': result.arm}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, ['endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8']))
print(json.dumps(results, indent=2))
sys.exit(int(any(r['rc'] for r in results)))
