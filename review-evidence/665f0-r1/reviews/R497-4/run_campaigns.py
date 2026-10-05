#!/usr/bin/env python3
"""Focused R497-4 receipts. Invoke: python3 run_campaigns.py REPO PACKET VERILATOR.
All processes are joined in the foreground. At most 16 compiler jobs:
mailbox campaign 3 x 4, co-simulation 2, firmware 1, contract checks 1.
Disposable copies and temporary files stay under PACKET/scratch.
"""
import concurrent.futures, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time
repo, packet, simulator = map(pathlib.Path, sys.argv[1:4])
repo, packet, simulator = repo.resolve(), packet.resolve(), simulator.resolve()
scratch = packet / 'scratch'
(scratch/'tmp').mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch/'tmp'), VERILATOR=str(simulator))
copy = scratch/'mailbox-tree'
for rel in ('hdl/milan/mailbox','tb/verilator/mbx','tb/common','sw/firmware/ctrl'):
    shutil.copytree(repo/rel, copy/rel, ignore=shutil.ignore_patterns('__pycache__','obj_*'), dirs_exist_ok=True)
version = subprocess.check_output([str(simulator),'--version'],text=True).strip()
assert 'Verilator 5.050 ' in version, version
(packet/'simulator-identity.txt').write_text(version+'\nlauncher sha256 '+hashlib.sha256(simulator.read_bytes()).hexdigest()+'\n')
vflags = '--cc --exe --build -j 2 --top-module tb_mbx_top -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I'+str(copy/'sw/firmware/ctrl/mbx')+'"'
commands = [
 ('firmware',[sys.executable,'-B','sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--build-dir',str(scratch/'firmware')],repo),
 ('mailbox-mutants',[sys.executable,'-B','mutants.py','--jobs','3','--keep',str(scratch/'mailbox-mutants')],copy/'tb/verilator/mbx'),
 ('cosim',['make','-j16','run-cosim','VERILATOR='+str(simulator),'VFLAGS='+vflags],copy/'tb/verilator/mbx'),
 ('contract',[sys.executable,'-B','sw/mailbox/gen_mailbox.py','--check','--crosscheck','--selftest'],repo)
]
def run(item):
    name,argv,cwd=item
    start=time.monotonic()
    with (scratch/(name+'.raw.log')).open('w') as log:
        result=subprocess.run(argv,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=540)
    data=(scratch/(name+'.raw.log')).read_text()
    # Public receipts preserve output except local source/build/launcher prefixes.
    data=data.replace(str(copy),'$SCRATCH/mailbox-tree').replace(str(repo),'$REPO').replace(str(scratch),'$SCRATCH').replace(str(simulator),'$VERILATOR')
    data=re.sub(r'/home/[^\s]+/usr/share/verilator', '$SIMULATOR_ROOT', data)
    (packet/(name+'.log')).write_text(data)
    (packet/(name+'.rc')).write_text(str(result.returncode)+'\n')
    print(name,'rc',result.returncode,'seconds',round(time.monotonic()-start,2),flush=True)
    return name,result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,commands))
(packet/'campaign-results.json').write_text(json.dumps(dict(results),indent=2)+'\n')
sys.exit(int(any(rc for _,rc in results)))
