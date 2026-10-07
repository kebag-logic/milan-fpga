#!/usr/bin/env python3
"""Focused review runs. All generated sources and binaries stay in scratch."""
import argparse
import shutil
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['positive', 'plants'])
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--jobs', type=int, default=4)
args = ap.parse_args()
root = args.repo.resolve()
packet = args.packet.resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
from ctrl_build import CTRL, Tree
import fw_gtest
from srp_arms import arm_srp

scratch = packet / 'scratch' / args.mode
scratch.mkdir(parents=True, exist_ok=True)
receipts = packet / args.mode
receipts.mkdir(exist_ok=True)
build = fw_gtest.Build(jobs=args.jobs)
lw = root / 'third_party/lwSRP'

# Independently selected reversals of the repaired decisions. Compilation
# failures never count as detection. Tests must execute and fail by name.
plants = [
    ('attach-level', 'm->ifs[n].link = mbx_link_up(n);',
     'm->ifs[n].link = false;', 'ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord'),
    ('recover-level', 'if (i->link != link)',
     'if (i->link && !link)', 'CancelledLinkRecordRecoversFromLevelAndFencesOldReceive'),
    ('shared-state', 'replacement.declared |= r->declared;',
     'replacement.declared = 0;', 'SharedRebindKeepsOnlyTheRemainingEligibleRequest'),
    ('consecutive-shared-state', 'replacement.declared |= r->declared;',
     'replacement.declared = 0;', 'ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation'),
    ('last-vid-user', 'if (old.vid != i->domain.vid &&',
     'if (old.vlan_requested && old.vid != i->domain.vid &&', 'LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder'),
    ('old-domain', 'i->msrp = NULL; i->mvrp = NULL; i->domain_owed = false;',
     'i->msrp = NULL; i->mvrp = NULL;', 'RefusedPeerDomainDoesNotSurviveLinkRestart'),
    ('old-vlan', 'i->sinks[k].vlan_requested = false; i->sinks[k].vlan_sent = false;',
     '(void)k;', 'SinkVlanRedeclaredBeforeReadyAfterLinkRestart'),
    ('representative-vlan', 'if (r->desired != 2 || r->vlan_sent)',
     'if (r->desired != 2 || s->vlan_sent)', 'SharedReadyWaitsForTheMatchingBindingsOwnVlan'),
    ('drop-shared-listener', 'if (!has_sink(i,&old,true))',
     'if (old.bound)', 'SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind'),
]

failed = False
if args.mode == 'positive':
    tree = Tree(CTRL, scratch / 'build', scratch / 'reuse', build)
    for interfaces in (1, 2):
        for suite in ('srp_mbx.cpp', 'srp_walk.cpp', 'srp_latency.cpp', 'srp_debug.cpp'):
            result = arm_srp(tree, lw, interfaces, debug=suite == 'srp_debug.cpp', test=suite)
            (receipts / f'{suite}-if{interfaces}.log').write_text(result.log)
            print(f'{suite} interfaces={interfaces} rc={result.rc}', flush=True)
            failed |= bool(result.rc)
else:
    src = scratch / 'ctrl'
    for name, old, new, test in plants:
        shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        target = src / 'srp/srp_mbx.c'
        original = target.read_text()
        assert original.count(old) == 1, name
        target.write_text(original.replace(old, new))
        result = arm_srp(Tree(src, scratch / 'build', scratch / 'reuse', build), lw, 2,
                         test=('srp_mbx.cpp', 'Srp.' + test))
        (receipts / f'{name}.log').write_text(result.log)
        caught = result.rc == 1 and ('[FAIL] Srp.' + test + ':') in result.log
        print(f'{name}: {"KILLED" if caught else "SURVIVED"}; test=Srp.{test}; rc={result.rc}', flush=True)
        failed |= not caught
print('RESULT: ' + ('FAIL' if failed else 'PASS'))
sys.exit(int(failed))
