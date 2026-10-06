#!/usr/bin/env python3
"""Run independent focused campaigns concurrently and join every child in foreground."""
import argparse,concurrent.futures,io,json,os,pathlib,subprocess,tarfile,time
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args()
root=a.source.resolve();packet=a.packet.resolve();scratch=packet/'scratch';scratch.mkdir(exist_ok=True)
tree=scratch/'head';tree.mkdir(exist_ok=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert head=='75c4eee4589e9317aca3d07b91f94a38b4cc86af'
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=root))) as t:t.extractall(tree,filter='data')
env=os.environ.copy();env['TMPDIR']=str(scratch);env['MAKEFLAGS']='-j16';env['PYTHONDONTWRITEBYTECODE']='1'
v=str(packet/'scripts/limited-simulator.py')
names=['cancel_one_per_command','report_fail_ignores_probe','report_rsp_ignores_probe','owner_turns_dropped','settle_dropped','depth_shared','depth_not_keyed','registry_tag_port_bits','monitor_tag_port_bits','expiry_port_dropped']
jobs=[('registry-controls', ['python3','tb/pp_top/notify_mutants.py','--output',str(packet/'receipts/registry-controls'),'--verilator',v,'--jobs','2','--only',*names],tree),
('top-controls',['python3','tb/pp_top/notify_mutants.py','--output',str(packet/'receipts/top-controls'),'--verilator',v,'--jobs','1','--only','rgy_port_from_latest_frame','dereg_matches_other_port'],tree),
('registry-suite',['make','-j16','run','VERILATOR='+v],tree/'tb/aecp_notify'),
('adp-suite',['make','-j16','run','VERILATOR='+v],tree/'tb/adp_engine'),
('interface-guards',['make','-j16','if-guards','VERILATOR='+v],tree/'tb/pp_top')]
def run(job):
 name,cmd,cwd=job; start=time.time();log=packet/'receipts'/f'{name}.log'
 with log.open('w') as f:
  f.write(json.dumps({'command':cmd,'cwd':str(cwd),'head':head})+'\n');f.flush()
  try:rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=1800).returncode
  except subprocess.TimeoutExpired:rc=124
 (packet/'receipts'/f'{name}.rc').write_text(str(rc)+'\n')
 result={'name':name,'rc':rc,'seconds':round(time.time()-start,2)};print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(run,jobs))
(packet/'receipts/focused-summary.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(x['rc'] for x in results))
