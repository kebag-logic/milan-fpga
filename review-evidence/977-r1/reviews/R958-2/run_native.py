#!/usr/bin/env python3
"""Focused native re-review checks; four concurrent builds, four compiler jobs each."""
import concurrent.futures
import os
from pathlib import Path
import sys
import traceback
root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build, ctrl_arms, srp_arms, fw_gtest

def one(name):
    out = packet / 'scratch' / name
    out.mkdir(parents=True, exist_ok=True)
    tree = ctrl_build.Tree(ctrl_build.CTRL, out, out / 'reuse', fw_gtest.Build(jobs=4))
    try:
        if name == 'native-loop':
            result = ctrl_arms.arm_port(tree)
        else:
            point = srp_arms.DEFAULT_ENTITY if name.endswith('1x1') else srp_arms.ENTITY_8X8
            test = ('test_acmp_mbx.cpp', 'SrpBinding.*') if name.startswith('native-binding') else (
                'srp_mbx.cpp', 'Srp.TheDrainChargesARecordTheTalkersItsVectorsCanRegister:SrpEarlyTalker.*')
            result = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', 1, test=test, config=point)
        log, rc = result.log, result.rc
    except Exception:
        log, rc = traceback.format_exc(), 2
    (packet / f'{name}.log').write_text(log)
    (packet / f'{name}.rc').write_text(f'{rc}\n')
    return name, rc

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(one, ['native-loop', 'native-charge-1x1', 'native-charge-8x8', 'native-binding-8x8']))
for name, rc in results:
    print(name, rc)
sys.exit(int(any(rc for _, rc in results)))
