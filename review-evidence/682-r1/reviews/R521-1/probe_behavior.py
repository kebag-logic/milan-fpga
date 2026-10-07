#!/usr/bin/env python3
from public_text import toolchain_paths
"""Parent notification seam and old-RTL negative controls in disposable trees."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root=Path.cwd();packet=Path(__file__).resolve().parent;scratch=packet/'scratch'
verilator=sys.argv[1]
env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1',VERILATOR=verilator,VERILATOR_JOBS='4',PYTHONHASHSEED='0')
parent=scratch/'parent-notify'
if not parent.exists():
    subprocess.run(['git','clone','--shared','--no-checkout',str(root),str(parent)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    subprocess.run(['git','checkout','--detach','5428b044176f95248e6916dc00dd89c0df154078'],cwd=parent,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for sub in ('protocol-processor','gptp-processor','third_party/verilog-axis'):
        subprocess.run(['git','config',f'submodule.{sub}.url',str(root/sub)],cwd=parent,check=True)
        subprocess.run(['git','-c','protocol.file.allow=always','submodule','update','--init',sub],cwd=parent,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def run(name,cmd,cwd,expected):
    start=time.monotonic()
    with (packet/(name+'.log')).open('wb') as log:
        rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (packet/(name+'.rc')).write_text(str(rc)+'\n')
    raw=(packet/(name+'.log')).read_bytes().replace(str(scratch).encode(),b'$SCRATCH').replace(str(root).encode(),b'$CANDIDATE').replace(verilator.encode(),b'$PINNED_VERILATOR')
    raw=toolchain_paths(raw)
    (packet/(name+'.log')).write_bytes(raw)
    r={'name':name,'command':cmd,'rc':rc,'expected':expected,'seconds':round(time.monotonic()-start,2),'sha256':hashlib.sha256(raw).hexdigest()}
    print(json.dumps(r),flush=True)
    return r

def faults():
    pp=scratch/'processor-focused'
    for path in ('hdl/aecp/KL_aecp_notify.sv','hdl/srp/KL_srp_talker_fsm.sv','hdl/srp/KL_srp_listener_fsm.sv'):
        old=subprocess.check_output(['git','-C',str(root/'protocol-processor'),'show','ead8036035affd53ef4b29979190f2f4f67084c0:'+path])
        (pp/path).write_bytes(old)
    return [run('notify-old-rtl',['make','-j16','run'],pp/'tb/aecp_notify',2),
            run('srp-old-rtl',['make','-j16','run'],pp/'tb/srp_stream_fsms',2)]

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    future=pool.submit(faults)
    records=[run('parent-notify',['make','-j16','notify','VERILATOR_JOBS=4'],parent/'tb/verilator/milan_dp',0)]
    records += future.result()
(packet/'behavior-probes.json').write_text(json.dumps(records,indent=2)+'\n')
raise SystemExit(any(x['rc']!=x['expected'] for x in records))
