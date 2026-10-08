#!/usr/bin/env python3
import argparse,sys,shutil,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['native','plants','independent','prior']);ap.add_argument('--interfaces',type=int,required=True);ap.add_argument('--source',type=Path,default=Path.cwd());ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
r=a.source.resolve();p=a.packet.resolve();sys.path.insert(0,str(r/'sw/firmware/ctrl/test'))
import ctrl_build,srp_arms,srp_mutants,fw_gtest
out=p/'scratch'/f'{a.mode}-if{a.interfaces}';out.mkdir(parents=True,exist_ok=True)
lw=r/'third_party/lwSRP'; tree=ctrl_build.Tree(ctrl_build.CTRL,out/'build',out/'reuse',fw_gtest.Build(jobs=a.jobs))
if a.mode=='plants':
    srp_mutants.DEFECTS=tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(('four-way-','binding-','feedback-','srp-bound-','srp-term-','srp-poll-extra','srp-send-extra')))
    sys.exit(int(srp_mutants.campaign(out,lw,jobs=a.jobs,interfaces=a.interfaces)))
if a.mode in ('independent','prior'):
    td=out/'tests';shutil.copytree(ctrl_build.HERE,td,dirs_exist_ok=True)
    headers=[p/'scripts/independent_feedback.hpp'] if a.mode=='independent' else [p/'scripts/prior/probe_tk_registered.hpp',p/'scripts/prior/probe_invalid_vid.hpp']
    with (td/'test_acmp_mbx.cpp').open('a') as f:
        for h in headers:f.write('\n'+h.read_text())
    srp_arms.HERE=td;suites=[('test_acmp_mbx.cpp','R533Feedback.R533*' if a.mode=='independent' else 'SrpBindingProbe.*:SrpBindingVidProbe.*')]
else:suites=['srp_mbx.cpp','srp_rx_retry.cpp','srp_app.cpp','test_acmp_mbx.cpp','srp_latency.cpp','srp_walk.cpp']
failed=False
for s in suites:
    o=srp_arms.arm_srp(tree,lw,a.interfaces,test=s);print(o.log,flush=True);failed=bool(o.rc) or failed
sys.exit(int(failed))
