#!/usr/bin/env python3
"""Portable focused review: python3 -B run_focus.py REPO [kind shape interfaces]."""
import concurrent.futures, os, shutil, subprocess, sys
from pathlib import Path
P=Path(__file__).resolve().parent
R=Path(sys.argv[1]).resolve()
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if len(sys.argv)==2:
    tasks=[('talker',s,i) for s,i in [('1x1',1),('8x8',1),('8x8',2)]]
    tasks += [('aecp',s,i) for s,i in [('1x1',1),('1x1',2),('8x8',1)]]
    tasks += [('mbx',s,i) for s in ['1x1','8x8'] for i in [1,2]]
    tasks += [('composed','8x8',2)]
    def run(t):
        tag='-'.join(map(str,t))
        with (P/(tag+'.log')).open('w') as f:
            try: rc=subprocess.run([sys.executable,'-B',str(__file__),str(R),*map(str,t)],stdout=f,stderr=subprocess.STDOUT,timeout=540).returncode
            except subprocess.TimeoutExpired: rc=124
        (P/(tag+'.rc')).write_text(str(rc)+'\n')
        return tag,rc
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(run,tasks))
    for tag,rc in results: print(tag,rc)
    sys.exit(any(rc for _,rc in results))
kind,shape,interfaces=sys.argv[2:]; interfaces=int(interfaces)
W=P/'scratch'/f'{kind}-{shape}-{interfaces}'
src=W/'ctrl'
shutil.copytree(R/'sw/firmware/ctrl',src,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
if kind=='aecp':
    shutil.copytree(R/'sw/firmware/ctrl_nvm',W/'ctrl_nvm',dirs_exist_ok=True)
    test=src/'test/test_aecp.cpp'
    with test.open('a') as f: f.write('\n'+(P/'link_reset_probe.cpp').read_text())
if kind=='talker':
    test=src/'test/srp_talker.cpp'
    # Restore the old test body only as a probe template: production and current tests stay unchanged.
    old=subprocess.check_output(['git','-C',str(R),'show','0d80f0ed:sw/firmware/ctrl/test/srp_talker.cpp'],text=True)
    start=old.index('TEST_F(Talker, ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest)')
    body=old[start:old.index('\n}\n',start)+3]
    assumption='    for (unsigned i=0;i<MBX_N_IF;++i) {\n        ASSERT_EQ(adapter.join_left[2u*i],0u) << "the join timer is idle as the count ends, so the hold stands in for it";\n    }\n'
    assert body.count(assumption)==1
    body=body.replace(assumption,'').replace('    advance(400);\n    untrace();','    advance(1500);\n    untrace();')
    with test.open('a') as f:
        f.write('\n'+(P/'reset_probe.cpp').read_text()+'\n'+(P/'phase_probe.cpp').read_text())
        for phase in range(300,1000,100):
            f.write('\n'+body.replace('ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest',f'LatestPhase{phase}').replace('advance(700);',f'advance({phase});'))
sys.path.insert(0,str(R/'sw/firmware/ctrl/test'))
import ctrl_build, srp_arms, aecp_arms, fw_gtest
srp_arms.HERE=src/'test'; aecp_arms.HERE=src/'test'
tree=ctrl_build.Tree(src,W/'build',W/'reuse',fw_gtest.Build(jobs=4))
cfg=R/'configs'/('endstation_ax7101_1x1_tdm8.yaml' if shape=='1x1' else 'endstation_ax7101_8x8.yaml')
if kind=='aecp':
    o=aecp_arms.core_arm(tree,cfg,interfaces,mode='app',selected='AppOutputs.*:App.SrpDeclarationChangeIsItsStreamOutputsNotice:App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed')
else:
    test=('srp_talker.cpp','*-ReviewerPhase.Held0:ReviewerPhase.Free0') if kind=='talker' else ('srp_mbx.cpp','Srp.*Build*:Srp.*Transmit*:Srp.AnOwedFrameComesBeforeTheBuild:Srp.TheJoinCountFollowsWhatABuildSent') if kind=='mbx' else ('test_acmp_mbx.cpp','SrpGate.*')
    o=srp_arms.arm_srp(tree,R/'third_party/lwSRP',interfaces,test=test,config=cfg)
print(o.log)
sys.exit(o.rc)
