#!/usr/bin/env python3
"""Foreground review runner. All disposable work stays below packet/scratch.

Usage: python3 run_focused.py --source CHECKOUT --packet PACKET --simulator PATH --jobs 4
Every child is waited for; no detached process is created. At most four simulations
or builds run together, each compiler build limited to two workers.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--simulator', type=Path, required=True)
p.add_argument('--jobs', type=int, required=True)
a = p.parse_args()
assert 1 <= a.jobs <= 4
scratch = a.packet / 'scratch'
receipts = a.packet / 'receipts' / 'focused'
receipts.mkdir(parents=True, exist_ok=True)
wrapper = scratch / 'limited-simulator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,x in enumerate(a[:-1]):\n if x in ("-j","--build-jobs"): a[i+1]="2"\nos.execv(' + repr(str(a.simulator)) + ',[' + repr(str(a.simulator)) + ']+a)\n')
wrapper.chmod(0o755)
env = dict(os.environ, VERILATOR=str(wrapper), TMPDIR=str(scratch), MAKEFLAGS='-j16', PYTHONDONTWRITEBYTECODE='1')

jobs = [
 ('top-default', 'srp_top', '', None),
 ('fsm-default', 'srp_stream_fsms', 'suite', None),
 ('second-lv-default', 'srp_top', '', 'lv-second-lv-ends'),
 ('never-ends-default', 'srp_top', '', 'lv-never-ends'),
 ('original-order-top', 'srp_top', 'lvcoll', 'lv-expiry-masked'),
 ('missed-collision-top', 'srp_top', 'lvcoll', 'lv-sweep-misses-collision'),
 ('original-order-fsm', 'srp_stream_fsms', 'suite', 'lv-expiry-masked'),
 ('expiry-last-fsm', 'srp_stream_fsms', 'suite', 'lv-expiry-last'),
 ('expiry-dropped-fsm', 'srp_stream_fsms', 'suite', 'lv-expiry-dropped'),
]

def run(job):
    label,suite,group,mutant = job
    tree = scratch / label
    tree.mkdir(exist_ok=True)
    for path in ('hdl', 'tb/common', 'tb/srp_top', 'tb/srp_stream_fsms'):
        shutil.copytree(a.source/path, tree/path, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('obj_*','__pycache__'))
    log = receipts / (label+'.log')
    start=time.monotonic()
    with log.open('w') as out:
        print('head='+subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.source,text=True).strip(),file=out,flush=True)
        if mutant:
            patch=a.source/'tb/srp_top/mutations'/f'{mutant}.patch'
            for flags in (['--check'],[]):
                subprocess.run(['git','apply',*flags,str(patch)],cwd=tree,stdout=out,stderr=subprocess.STDOUT,check=True)
        cmd=['make','-j16','run',f'RUN_ARGS={group}']
        print('command='+repr(cmd),file=out,flush=True)
        r=subprocess.run(cmd,cwd=tree/'tb'/suite,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=580)
    (receipts/(label+'.rc')).write_text(str(r.returncode)+'\n')
    text=log.read_text()
    failures=[s for s in text.splitlines() if s.startswith('FAIL:')]
    tally=[s for s in text.splitlines() if 'checks:' in s and 'PASS' in s][-1:]
    result={'label':label,'rc':r.returncode,'seconds':round(time.monotonic()-start,2),'failures':len(failures),'tally':tally,'tags':sorted({s.split(':')[1].strip() for s in failures})}
    print(json.dumps(result),flush=True)
    return result

with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
    results=list(pool.map(run,jobs))
(receipts/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['tally'] for x in results), 'Missing completion tally'
assert all(x['rc']==0 for x in results[:2]), 'Positive control failed'
assert all(x['rc']!=0 and x['failures'] for x in results[2:]), 'Mutant survived'
