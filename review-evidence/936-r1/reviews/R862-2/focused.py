#!/usr/bin/env python3
"""Focused regression and mutation probes, using repository recipes.
Usage: python3 -B focused.py CHECKOUT PACKET [all|app|srp1|srp2]
Three foreground-supervised workers use four compile jobs each. All disposable
files stay in PACKET/scratch. Raw test logs are copied into PACKET/receipts.
"""
import concurrent.futures
import os
from pathlib import Path
import shutil
import subprocess
import sys

root, packet = (Path(x).resolve() for x in sys.argv[1:3])
mode = sys.argv[3] if len(sys.argv) > 3 else 'all'
receipts = packet / 'receipts'
receipts.mkdir(exist_ok=True)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
temporary = packet / 'scratch/tmp'
temporary.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(temporary)
if mode == 'all':
    def launch(which):
        with (receipts / (which + '.log')).open('w') as log:
            result = subprocess.run([sys.executable, '-B', __file__, str(root), str(packet), which],
                                    stdout=log, stderr=subprocess.STDOUT)
        (receipts / (which + '.rc')).write_text(str(result.returncode) + '\n')
        return which, result.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(launch, ('app', 'srp1', 'srp2')))
    for which, rc in results:
        print(which, 'rc', rc)
    raise SystemExit(any(rc for _, rc in results))

sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import fw_gtest
from ctrl_build import Tree, CTRL, STACK
work = packet / 'scratch' / mode
tree = Tree(CTRL, work / 'baseline', work / 'reuse', fw_gtest.Build(jobs=4), STACK)
if mode == 'app':
    import aecp_arms as arms
    import aecp_mutants as mutants
    selected = 'App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed:App.SrpDeclarationChangeIsItsStreamOutputsNotice'
    config = root / 'configs/endstation_ax7101_1x1_tdm8.yaml'
    outcomes = [arms.core_arm(tree, config, n, mode='app', selected=selected) for n in (1, 2)]
    # Verify the full inventory and diagnostic-reader controls before selecting
    # one plant; selection is not a claim to rerun the full campaign.
    mutants.controls()
    mutants.DEFECTS = tuple(d for d in mutants.DEFECTS if d.name == 'app-output-notice-owed-unreported')
    mutants.controls = lambda: None
    campaign = lambda: mutants.campaign(work / 'plants', jobs=4)
else:
    import srp_arms as arms
    import srp_mutants as mutants
    interfaces = int(mode[-1])
    selected = ('SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource:'
                'SrpGate.F936BThePassThatTakesTheRecordOwesItsNotice:'
                'SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface')
    lw = root / 'third_party/lwSRP'
    outcomes = [arms.arm_srp(tree, lw, interfaces, test=('test_acmp_mbx.cpp', selected))]
    names = {'talker-notice-owed-unreported', 'binding-poll-adds-access'}
    mutants.DEFECTS = tuple(d for d in mutants.DEFECTS if d.name in names)
    assert len(mutants.DEFECTS) == 2
    campaign = lambda: mutants.campaign(work / 'plants', lw, jobs=4, interfaces=interfaces)
for n, result in enumerate(outcomes):
    (receipts / f'{mode}-baseline-{n}.log').write_text(result.log)
    print(f'{result.arm}: baseline rc {result.rc}', flush=True)
    assert result.rc == 0, result.log
failed = campaign()
for path in (work / 'plants').glob('*.log'):
    shutil.copyfile(path, receipts / f'{mode}-{path.name}')
print(f'{mode}: focused campaign failed={failed}', flush=True)
raise SystemExit(bool(failed))
