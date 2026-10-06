#!/usr/bin/env python3
"""Focused controls affected by the merged SRP and originator files; all-arm planting audit."""
import concurrent.futures,importlib.util,json,os,pathlib,subprocess,sys,tempfile
p=pathlib.Path(__file__).resolve().parents[1];root=p/'scratch/source';receipt=p/'receipts'
env=os.environ.copy();env.update(TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1',REVIEW_LOCKDIR=str(p/'scratch/build-locks'),MAKEFLAGS='-j16',VERILATOR=str(p/'scripts/bounded-verilator.py'))
os.environ.update(env);sys.path.insert(0,str(root/'tb/pp_top'))
import notify_mutants as nm
records=[]
for m in nm.MUTANTS:
 with tempfile.TemporaryDirectory(prefix='plant-only-',dir=p/'scratch') as temp:
  tree=pathlib.Path(temp)
  for rel,_,_ in m.edits:
   f=tree/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((root/rel).read_bytes())
  reason=nm.plant(tree,m.edits);records.append({'name':m.name,'planted':not reason,'reason':reason})
(receipt/'all-notify-planting.json').write_text(json.dumps(records,indent=2)+'\n')
assert all(x['planted'] for x in records)
def run(name,cmd):
 with (receipt/(name+'.log')).open('w') as f:
  f.write('COMMAND '+json.dumps(cmd)+'\n');f.flush();r=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
 (receipt/(name+'.rc')).write_text(str(r.returncode)+'\n');print(name,r.returncode,flush=True);return r.returncode
commands=[('originator-controls',[sys.executable,'tb/pp_top/notify_mutants.py','--output',str(receipt/'originator-controls'),'--verilator',env['VERILATOR'],'--jobs','2','--only','inflight_highest_free_id','inflight_match_ignores_seq','inflight_cancel_keeps_timer','inflight_shared_seq']),('srp-controls',[sys.executable,'tb/srp_top/mutants.py','--output',str(receipt/'srp-controls'),'--jobs','2','--only','lv-expiry-masked,lv-expiry-last,lv-expiry-dropped,lv-sweep-misses-collision'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(lambda x:run(*x),commands))
sys.exit(int(any(results)))
