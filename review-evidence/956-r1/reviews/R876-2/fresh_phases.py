#!/usr/bin/env python3
"""Run the original seven phase probes, each in a fresh process after run_focus.py."""
import concurrent.futures,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
points=[('1x1',1),('8x8',1),('8x8',2)]
def run(point):
    shape,n=point; tag=f'fresh-phases-{shape}-{n}'
    exe=next((P/'scratch'/f'talker-{shape}-{n}'/'build').glob('srp-*/suite'))
    rc=0
    with (P/(tag+'.log')).open('w') as f:
        for phase in range(300,1000,100):
            code=subprocess.run([str(exe),f'--gtest_filter=Talker.LatestPhase{phase}'],stdout=f,stderr=subprocess.STDOUT,timeout=30).returncode
            rc|=code
    (P/(tag+'.rc')).write_text(str(rc)+'\n')
    print(tag,rc)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    codes=list(pool.map(run,points))
raise SystemExit(any(codes))
