#!/usr/bin/env python3
"""Replay the seven new named defects, preserving every raw failure. Args: checkout packet compiler-wrapper."""
import concurrent.futures as cf
import importlib.util
import os
from pathlib import Path
import sys
repo,packet,compiler=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve(),sys.argv[3]
os.environ['VERILATOR']=compiler
os.environ['TMPDIR']=str(packet/'scratch')
sys.path.insert(0,str(repo/'tb/verilator/mbx'))
spec=importlib.util.spec_from_file_location('review_mutants',repo/'tb/verilator/mbx/mutants.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
names=['rx-drop-instead-of-hold','rx-hold-behind-a-held-frame','rx-held-record-never-committed',
       'rx-next-frame-over-the-held-record','rx-tail-inside-the-held-record-frees-space',
       'rx-refill-in-the-header-clock-missed','rx-refill-in-the-header-clock-missed-axil']
arms=[a for a in m.ARMS if a.name in names]
assert len(arms)==7
root=packet/'scratch/mutations'
def run(a):
    rc,log=m.build_and_run(m.plant(a,root),root/a.name,a.host,a.ifs)
    (packet/(a.name+'.log')).write_text(log)
    fails=[x for x in log.splitlines() if '[FAIL]' in x]
    ok=rc==1 and any(a.needle in x for x in fails)
    return f'{a.name}: caught={ok} rc={rc} expected={a.needle}',ok
with cf.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,arms))
text='\n'.join(x[0] for x in results)+'\n'
(packet/'mutations.log').write_text(text); print(text)
rc=int(not all(x[1] for x in results));(packet/'mutations.rc').write_text(str(rc)+'\n');sys.exit(rc)
