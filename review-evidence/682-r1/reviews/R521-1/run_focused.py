#!/usr/bin/env python3
from public_text import toolchain_paths
"""Run bounded focused checks; no source checkout edits or detached jobs."""
import argparse
import concurrent.futures
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time

p=argparse.ArgumentParser()
p.add_argument('group',choices=['static','units'])
p.add_argument('--verilator',required=True)
a=p.parse_args()
root=Path.cwd();packet=Path(__file__).resolve().parent
scratch=packet/'scratch';scratch.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',VERILATOR=a.verilator,VERILATOR_JOBS='4')
ver=subprocess.check_output([a.verilator,'--version'],env=env,text=True).strip()
assert 'Verilator 5.050 ' in ver
records=[]

def run(name,cmd,cwd=root):
    start=time.monotonic()
    with (packet/(name+'.log')).open('wb') as log:
        rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (packet/(name+'.rc')).write_text(str(rc)+'\n')
    raw=(packet/(name+'.log')).read_bytes()
    # Public logs use placeholders for local paths.
    raw=raw.replace(str(scratch).encode(),b'$SCRATCH').replace(str(root).encode(),b'$CANDIDATE').replace(a.verilator.encode(),b'$PINNED_VERILATOR')
    raw=toolchain_paths(raw)
    (packet/(name+'.log')).write_bytes(raw)
    record={'name':name,'command':[x.replace(str(scratch),'$SCRATCH').replace(str(root),'$CANDIDATE') for x in cmd],
            'cwd':str(cwd).replace(str(scratch),'$SCRATCH').replace(str(root),'$CANDIDATE'),
            'rc':rc,'seconds':round(time.monotonic()-start,2),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    print(json.dumps(record),flush=True)
    return record

if a.group=='static':
    tasks=[
      ('baseline-selftest',['python3','syn/ooc/pp_baseline.py','--selftest']),
      ('baseline-mutants',['python3','syn/ooc/pp_baseline_mutants.py']),
      ('resource-baseline',['python3','syn/ooc/pp_resource_gate.py','check-baseline']),
      ('capture',['python3','scripts/check_nvm_capture.py']),
      ('ports',['python3','scripts/check_port_contracts.py']),
      ('naming',['python3','scripts/measure_naming.py','--check']),
      ('submodule-docs',['python3','scripts/check_submodule_docs.py']),
      ('integrator-params',['python3','protocol-processor/scripts/check-integrator-params.py']),
      ('source-list',['python3','scripts/pp_srcs.py','--check']),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records=list(pool.map(lambda t:run(*t),tasks))
else:
    dest=scratch/'processor-focused'
    dest.mkdir(exist_ok=True)
    archive=subprocess.check_output(['git','-C','protocol-processor','archive','HEAD'])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(dest,filter='data')
    # These archived Makefiles hard-code -j 0. Change build concurrency only.
    for suite in ('aecp_notify','srp_stream_fsms'):
        mf=dest/'tb'/suite/'Makefile'
        source=mf.read_text(); assert '--build -j 0' in source
        mf.write_text(source.replace('--build -j 0','--build -j 4'))
    tasks=[('notify-unit',['make','-j16','run'],dest/'tb/aecp_notify'),
           ('srp-unit',['make','-j16','run'],dest/'tb/srp_stream_fsms')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        records=list(pool.map(lambda t:run(*t),tasks))
result={'version':ver,'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'group':a.group,'records':records}
(packet/(a.group+'-checks.json')).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in records))
