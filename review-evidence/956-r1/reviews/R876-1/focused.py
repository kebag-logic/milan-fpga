#!/usr/bin/env python3
"""Run focused tests on an exact source tree; all disposable files stay in scratch."""
import argparse
import shutil
import sys
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('repo',type=Path)
p.add_argument('kind',choices=['srp','aecp','composed','reset','phases'])
p.add_argument('shape',choices=['1x1','8x8'])
p.add_argument('interfaces',type=int)
p.add_argument('--jobs',type=int,default=4)
a=p.parse_args()
repo=a.repo.resolve()
packet=Path(__file__).resolve().parent
tag=f'{a.kind}-{a.shape}-if{a.interfaces}'
work=packet/'scratch'/tag
work.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import ctrl_build
import srp_arms
import aecp_arms
import fw_gtest
src=repo/'sw/firmware/ctrl'
if a.kind in ('reset','phases'):
    src=work/'ctrl'
    shutil.copytree(repo/'sw/firmware/ctrl',src,dirs_exist_ok=True)
    test=src/'test/srp_talker.cpp'
    if a.kind=='reset':
        test.write_text(test.read_text()+'\n'+(packet/'reset_probe.cpp').read_text())
    else:
        original=test.read_text()
        start=original.index('TEST_F(Talker, ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest)')
        end=original.index('\n}\n',start)+3
        body=original[start:end]
        assumption='    for (unsigned i=0;i<MBX_N_IF;++i) {\n        ASSERT_EQ(adapter.join_left[2u*i],0u) << "the join timer is idle as the count ends, so the hold stands in for it";\n    }\n'
        assert body.count(assumption)==1
        body=body.replace(assumption,'').replace('    advance(400);\n    untrace();','    advance(1500);\n    untrace();')
        probes=[]
        for phase in range(300,1000,100):
            probes.append(body.replace('ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest',f'LatestPhase{phase}').replace('advance(700);',f'advance({phase});'))
        test.write_text(original+'\n'+'\n'.join(probes))
    srp_arms.HERE=src/'test'
tree=ctrl_build.Tree(src,work/'build',work/'reuse',fw_gtest.Build(jobs=a.jobs))
cfg=repo/'configs'/('endstation_ax7101_1x1_tdm8.yaml' if a.shape=='1x1' else 'endstation_ax7101_8x8.yaml')
if a.kind=='aecp':
    r=aecp_arms.core_arm(tree,cfg,a.interfaces,mode='app',selected='AppOutputs.*:App.SrpDeclarationChangeIsItsStreamOutputsNotice:App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed')
else:
    selection=('test_acmp_mbx.cpp','SrpGate.*') if a.kind=='composed' else ('srp_talker.cpp','Talker.RegistrationAfterLinkResetIsNoticed') if a.kind=='reset' else ('srp_talker.cpp','Talker.LatestPhase700') if a.kind=='phases' else 'srp_talker.cpp'
    r=srp_arms.arm_srp(tree,repo/'third_party/lwSRP',a.interfaces,test=selection,config=cfg)
    if a.kind=='phases':
        exe=next((work/'build').glob('srp-*/suite'))
        logs=[]
        failed=False
        for phase in range(300,1000,100):
            ok,log=fw_gtest.run_binary(exe,[f'--gtest_filter=Talker.LatestPhase{phase}'])
            failed|=not ok
            logs.append(log)
        r=ctrl_build.Outcome(tag,int(failed),'\n'.join(logs))
(packet/(tag+'.log')).write_text(r.log)
(packet/(tag+'.rc')).write_text(str(r.rc)+'\n')
print(r.log)
raise SystemExit(r.rc)
