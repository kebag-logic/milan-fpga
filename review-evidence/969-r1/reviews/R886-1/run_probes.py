#!/usr/bin/env python3
"""Run review probes without modifying the checkout: CHECKOUT PACKET."""
import concurrent.futures
import json
from pathlib import Path
import shutil
import sys
import traceback
root, packet = (Path(x).resolve() for x in sys.argv[1:3])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build as cb
import srp_arms
import fw_gtest

def run(spec):
    shape, version=spec
    name=f'probe-{shape}-{version}'
    out=packet/'scratch'/name
    out.mkdir(parents=True,exist_ok=True)
    src=cb.CTRL if version=='head' else packet/'scratch/focused/base-src'
    test=out/'probes.cpp'
    # The base control needs no fields introduced by the fix.
    text=(packet/'probes.cpp').read_text().replace('    ASSERT_EQ(adapter.kept_count[0],1u);\n','')
    test.write_text(text)
    tree=cb.Tree(src,out,out/'reuse',fw_gtest.Build(jobs=4))
    cfg=srp_arms.DEFAULT_ENTITY if shape=='1x1' else srp_arms.ENTITY_8X8
    try:
        selected='SrpEarlyTalker.Review*' if version=='head' else 'SrpEarlyTalker.ReviewUnbindRebindControlEveryInput'
        result=srp_arms.arm_srp(tree,root/'third_party/lwSRP',1,test=(str(test),selected),config=cfg)
        rc,log=result.rc,result.log
    except Exception:
        rc,log=2,traceback.format_exc()
    (packet/(name+'.log')).write_text(log)
    (packet/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,rc,flush=True)
    return {'name':name,'rc':rc}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,[(s,v) for s in ('1x1','8x8') for v in ('head','base')]))
(packet/'probe-results.json').write_text(json.dumps(results,indent=2)+'\n')
