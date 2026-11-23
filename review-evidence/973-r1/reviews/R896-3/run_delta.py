#!/usr/bin/env python3
"""Focused prior-head regression and link plants; at most 16 compiler jobs."""
import concurrent.futures, json, shutil, subprocess, sys
from pathlib import Path
root, packet = [Path(x).resolve() for x in sys.argv[1:3]]
sys.dont_write_bytecode=True
sys.path[:0]=[str(root/'sw/firmware/ctrl/test'),str(root/'sw/firmware/gtest')]
import fw_gtest, srp_arms, srp_mutants
from ctrl_build import Tree, CTRL
scratch=packet/'scratch'; tests=scratch/'delta-tests'; tests.mkdir(exist_ok=True)
for f in (CTRL/'test').iterdir():
    if f.is_file() and f.suffix in ('.cpp','.hpp','.h'): shutil.copy2(f,tests/f.name)
(tests/'probe_stale_mark.cpp').write_bytes((tests/'srp_link_pass.cpp').read_bytes()+(packet/'probe_stale_mark.cpp').read_bytes())
srp_arms.HERE=tests
prior=scratch/'delta-prior-ctrl'; shutil.copytree(CTRL,prior,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
for name in ['srp_mbx.c','srp_mbx.h']:
    (prior/'srp'/name).write_bytes(subprocess.check_output(['git','-C',str(root),'show','5759780f:sw/firmware/ctrl/srp/'+name]))
reset='        if (i->link != link) {\n            reset_interface(i);\n'
sink='        if (i->link_seen || !event->link_up) {\n            reset_interface(i);\n'
D=srp_mutants.Defect
srp_mutants.DEFECTS=tuple(d for d in srp_mutants.DEFECTS if d.name.startswith('link-pass-'))+(
 D('rv-poll-resets-on-register-up','SrpLinkPass.AfterTheEventsBeforeSrpsPoll',reset,'        if (i->link != link || (mbx_link_up(n) && !i->link)) {\n            reset_interface(i);\n',"SRP's poll reset the interface on a level no LINK had carried",suite='srp_link_pass.cpp'),
 D('rv-sink-double-reset','SrpLinkPass.InTheEvents',sink,sink+'            reset_interface(i);\n','resets the interface once',suite='srp_link_pass.cpp'))
def run(spec):
    mode,stem=spec; out=scratch/(mode+'-'+stem)
    if mode=='prior':
        r=srp_arms.arm_srp(Tree(prior,out,out/'reuse',fw_gtest.Build(jobs=4)),root/'third_party/lwSRP',1,test='probe_stale_mark.cpp',config=root/'configs'/(stem+'.yaml'))
        text=r.log; ok=r.rc==1 and all('[  FAILED  ] '+n in text for n in ['SrpLinkPassElided.AnElidedUpAuthorizesNoFreshFirstUp','SrpLinkPassElided.AnElidedUpAuthorizesNoFreshLaterUp','SrpLinkPass.AnElidedUpDoesNotAuthorizeAFreshUpInsideAPass'])
        (packet/(mode+'-'+stem+'.log')).write_text(text.replace(str(root),'<checkout>').replace(str(packet),'<packet>'))
        (packet/(mode+'-'+stem+'.rc')).write_text(str(r.rc)+'\n')
    else:
        ok=not srp_mutants.campaign(out,root/'third_party/lwSRP',jobs=4,interfaces=1,entity=stem)
        dest=packet/'plants'/stem;dest.mkdir(parents=True,exist_ok=True)
        for f in out.glob('*.log'):
            (dest/f.name).write_text(f.read_text().replace(str(root),'<checkout>').replace(str(packet),'<packet>'))
    return {'mode':mode,'shape':stem,'expected_result_verified':ok}
specs=[(m,s) for m in ['prior','plants'] for s in ['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8']]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(run,specs))
(packet/'delta-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2));sys.exit(int(not all(r['expected_result_verified'] for r in results)))
