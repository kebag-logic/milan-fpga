#!/usr/bin/env python3
"""Run the five recount trigger plants at both interface counts and at 8x8/1if.

Usage: python3 run_plants.py CHECKOUT PACKET [WORKER]
Each worker uses --jobs-equivalent 4 compilation jobs; 12 jobs maximum.
"""
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys
root, packet = (Path(x).resolve() for x in sys.argv[1:3])
if len(sys.argv)>3:
    sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
    import srp_mutants
    import srp_early_mutants
    name=sys.argv[3]
    names = {'feedback-early-reset-counted','feedback-early-end-unowed','feedback-early-unregistered-unowed','feedback-early-left-seen-unowed','feedback-early-refresh-counted-again'}
    srp_mutants.DEFECTS=tuple(d for d in srp_early_mutants.defects(srp_mutants.Defect) if d.name in names)
    out=packet/'scratch/plants'/name
    failed=srp_mutants.campaign(out, root/'third_party/lwSRP', jobs=4,
        interfaces=2 if name=='1x1-if2' else 1,
        entity='endstation_ax7101_8x8' if name=='8x8-if1' else '')
    receipts=packet/'plant-logs'/name
    receipts.mkdir(parents=True,exist_ok=True)
    for f in out.glob('*.log'): shutil.copyfile(f,receipts/f.name)
    sys.exit(int(failed))

def run(name):
    with (packet/(name+'-plants.log')).open('w') as log:
        rc=subprocess.run([sys.executable,__file__,str(root),str(packet),name],
                          stdout=log,stderr=subprocess.STDOUT).returncode
    (packet/(name+'-plants.rc')).write_text(str(rc)+'\n')
    print(name,rc,flush=True)
    return {'name':name,'rc':rc}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,['1x1-if1','1x1-if2','8x8-if1']))
(packet/'plants-results.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(r['rc'] for r in results))
