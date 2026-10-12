#!/usr/bin/env python3
import argparse,json,pathlib,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--simulator',required=True);a=ap.parse_args();p=a.packet.resolve();env=json.loads((p/'scratch/environment.json').read_text());tree=p/'scratch/fabric/tb/acmp_talker';sim=tree/'sim_main.cpp';orig=sim.read_text();needle='d->now_ms_i = t2 + T_DAFRESH + 1;';assert orig.count(needle)==1
identity=subprocess.check_output([a.simulator,'--version'],text=True);assert 'Verilator 5.050 ' in identity
flags='--cc --exe --build -j 16 --top-module KL_acmp_talker -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -I'+str(tree)+' -Wall -Wextra"'
rows=[]
try:
 for name,repl in [('stock',needle),('edge-15000','d->now_ms_i = t2 + T_DAFRESH;'),('edge-14999','d->now_ms_i = t2 + T_DAFRESH - 1;')]:
  sim.write_text(orig.replace(needle,repl))
  logpath=p/'scratch'/('fabric-'+name+'.log')
  with logpath.open('w') as log:r=subprocess.run(['make','-j16','run','VERILATOR='+a.simulator,'VFLAGS='+flags],cwd=tree,env=env,stdout=log,stderr=subprocess.STDOUT)
  body=logpath.read_text()
  if name=='edge-14999':assert r.returncode!=0 and 'D2 freshness lapse' in body
  else:assert r.returncode==0 and '1342 checks: 1342 PASS, 0 FAIL' in body
  rows.append(dict(case=name,rc=r.returncode));print(name,r.returncode,flush=True)
finally:sim.write_text(orig)
(p/'receipts/fabric-results.json').write_text(json.dumps(dict(identity=identity,results=rows),indent=2)+'\n')
