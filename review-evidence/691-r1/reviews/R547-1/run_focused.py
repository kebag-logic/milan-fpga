#!/usr/bin/env python3
"""Await independent focused checks, with at most two builds and four compiler jobs each."""
import concurrent.futures
import io
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tarfile
import time

repo=Path(sys.argv[1]).resolve()
real_sim=Path(sys.argv[2]).resolve()
packet=Path(__file__).resolve().parent
scratch=packet/'scratch'
native=scratch/'native'
if not (native/'.git').exists():
    if native.exists():
        shutil.rmtree(native)
    subprocess.run(['git','clone','--shared','--no-checkout',str(repo),str(native)],check=True)
    subprocess.run(['git','checkout','--detach','35fb2a95007ce6dd1ec4f51c2dcb793800623cfd'],cwd=native,check=True)
    for sub in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
        subprocess.run(['git','submodule','update','--init','--reference',str(repo/sub),'--',sub],cwd=native,check=True)
wrapper=scratch/'simulator'
wrapper.write_text('''#!/usr/bin/env python3
import os,sys
a=sys.argv[1:]; out=[]; i=0
while i<len(a):
    if a[i] in ('-j','--jobs','--build-jobs'):
        i+=2
    elif a[i].startswith('-j') or a[i].startswith('--jobs=') or a[i].startswith('--build-jobs='):
        i+=1
    else:
        out.append(a[i]); i+=1
os.execv(os.environ['REVIEW_SIMULATOR'], [os.environ['REVIEW_SIMULATOR'], *out, '-j', '4'])
''')
wrapper.chmod(0o755)
python=scratch/'venv/bin/python'
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
    PYTHON=str(python),MILAN_LITEX_PYTHON=str(python), TMPDIR=str(scratch),
    VERILATOR=str(wrapper),REVIEW_SIMULATOR=str(real_sim), MAKEFLAGS='-j16',
    PATH=str(python.parent)+':'+os.environ['PATH'])
tasks=[
 ('edge-oracle', scratch, [
  [str(wrapper),'--cc','--exe','--build','--top-module','oracle_top','-Wno-fatal','--Mdir',str(scratch/'obj_oracle'),str(scratch/'oracle_top.sv'),str(scratch/'candidate.v'),str(scratch/'original.v'),str(packet/'pad_oracle.cpp')],
  [str(scratch/'obj_oracle/Voracle_top')]]),
 ('standalone', native, [['bash','scripts/run_litex_sims.sh',str(scratch/'standalone')]]),
 ('runner-selftest',native,[['bash','scripts/run_litex_sims.sh','--selftest']]),
 ('rx-filter',native/'tb/verilator/rx_filter',[['make','-j16','run']]),
 ('eth-reset',native/'tb/verilator/eth_tx_reset',[['make','-j16']]),
 ('link-guard',native/'tb/verilator/link_guard',[['make','-j16']]),
 ('rmon',native/'tb/verilator/mac_rmon',[['make','-j16','full'],['make','-j16','nochk']]),
]

def run(task):
    name,cwd,commands=task
    start=time.monotonic()
    log=scratch/f'{name}.log'
    results=[]
    with log.open('w') as out:
        for command in commands:
            out.write('COMMAND '+json.dumps(command)+'\n');out.flush()
            r=subprocess.run(command,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=570)
            results.append(r.returncode)
            if r.returncode:break
    text=log.read_text().replace(str(scratch),'$SCRATCH').replace(str(repo),'$REPO').replace(str(packet),'$PACKET').replace(str(real_sim),'$SIMULATOR')
    (packet/f'{name}.log').write_text(text)
    (packet/f'{name}.rc').write_text(str(results[-1])+'\n')
    result={'check':name,'returncodes':results,'seconds':round(time.monotonic()-start,2)}
    print(json.dumps(result),flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(run,tasks))
(packet/'focused-results.json').write_text(json.dumps(results,indent=2)+'\n')
for path in (scratch/'standalone').glob('*.log'):
    (packet/f'standalone-{path.name}').write_text(path.read_text().replace(str(scratch),'$SCRATCH'))
assert all(all(rc==0 for rc in r['returncodes']) for r in results)
print('PASS: all focused commands completed; no child remains')
