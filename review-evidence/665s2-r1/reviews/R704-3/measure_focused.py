#!/usr/bin/env python3
"""Run focused native campaigns and the prior native driver concurrently."""
import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
root=Path(os.environ['REVIEW_ROOT']);packet=Path(os.environ['REVIEW_PACKET'])
def command(label,argv):
    start=time.monotonic()
    with (packet/(label+'.log')).open('w') as log:
        rc=subprocess.call(argv,stdout=log,stderr=subprocess.STDOUT)
    result=dict(returncode=rc,seconds=round(time.monotonic()-start,3))
    (packet/(label+'.rc.json')).write_text(json.dumps(result)+'\n')
    print(label,result,flush=True)
    return rc
def campaign(label,point):
    return command(label+'-focused',[sys.executable,'-B',str(root/'tb/verilator/ctrl_service_budget/run.py'),
        '--point',point,'--build-dir',str(packet/'scratch'/label),'--reuse-build','--jobs','6',
        '--groups','backlog,backlog-adp,backlog-adp-refill,backlog-owed,aecp,aecp-fanout',
        '--out',str(packet/'measurements'/label),'--record-budget-findings'])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures=[pool.submit(campaign,'A1','1x1'),pool.submit(campaign,'A8','8x8'),
             pool.submit(command,'prior-native-unmodified',[sys.executable,'-B',str(packet/'prior/probe_native_delta.py')])]
    results=[f.result() for f in futures]
raise SystemExit(bool(any(results)))
