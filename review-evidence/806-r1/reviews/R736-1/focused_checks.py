#!/usr/bin/env python3
"""Reproduce focused review checks; all child commands are joined, with raw logs."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
source=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(sys.argv[2]).resolve()
verilator=sys.argv[3]
work=packet/'scratch'/'probe'
receipts=packet/'focused'; receipts.mkdir(exist_ok=True)
def run(name, cmd, cwd):
    start=time.monotonic()
    with (receipts/(name+'.log')).open('w') as out:
        out.write('$ '+str(cmd)+'\n'); out.flush()
        rc=subprocess.run(cmd,cwd=cwd,stdout=out,stderr=subprocess.STDOUT).returncode
    (receipts/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,rc,round(time.monotonic()-start,2),flush=True)
    return rc
if not work.exists():
    subprocess.run(['git','clone','--shared','--no-checkout',str(source),str(work)],check=True)
    subprocess.run(['git','checkout','--detach','f99405af0b2caad46e84f50f8251ffbffaa80836'],cwd=work,check=True)
    for sub in ['gptp-processor','protocol-processor','third_party/verilog-axis','third_party/lwSRP','third_party/tsn-c-stack']:
        subprocess.run(['git','config','submodule.'+sub+'.url',str(source/sub)],cwd=work,check=True)
        subprocess.run(['git','-c','protocol.file.allow=always','submodule','update','--init',sub],cwd=work,check=True)
run('identity',[verilator,'--version'],work)
# One build at a time owns the 16 compiler slots. Executions use separate objects.
for name, folder, target in [('gptp','milan_dp','build-gptp'),('gptp-lat','milan_dp','build-gptp-lat')]:
    rc=run('build-'+name,['make','-j16','VERILATOR='+verilator,'VERILATOR_JOBS=16',target],work/'tb/verilator'/folder)
    if rc: sys.exit(rc)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    fs=[pool.submit(run,n,['make','-j16',t],work/'tb/verilator/milan_dp') for n,t in [('gptp','exec-gptp'),('gptp-lat','exec-gptp-lat')]]
    results=[f.result() for f in fs]
sys.exit(any(results))
