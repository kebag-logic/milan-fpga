#!/usr/bin/env python3
"""Export exact source, build focused bench, and grade independent ROM trials."""
import argparse,concurrent.futures,hashlib,importlib.util,json,os,pathlib,shutil,subprocess,sys,tarfile
ap=argparse.ArgumentParser();ap.add_argument('--source',type=pathlib.Path,required=True);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1];scratch=packet/'scratch';receipts=packet/'receipts/focused';receipts.mkdir(exist_ok=True)
head='ebc3b6bcd6e2c789c1c80c9e285193628567ea33'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.source,text=True).strip()==head
archive=scratch/'head.tar';archive.write_bytes(subprocess.check_output(['git','archive',head],cwd=a.source))
tree=scratch/'head';tree.mkdir(exist_ok=True)
with tarfile.open(archive) as t:t.extractall(tree,filter='data')
subprocess.run(['git','init','-q',str(tree)],check=True)
objects=subprocess.check_output(['git','rev-parse','--path-format=absolute','--git-path','objects'],cwd=a.source,text=True).strip()
(tree/'.git/objects/info/alternates').write_text(objects+'\n')
subprocess.run(['git','read-tree',head],cwd=tree,check=True)
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['TMPDIR']=str(scratch)
def run(cmd,cwd,log):
 with (receipts/log).open('w') as f:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 (receipts/(log+'.rc')).write_text(str(r.returncode)+'\n');return r.returncode
sim=str(packet/'scripts/simulator.py')
def build():return run(['make','-j16','gsi-build','VERILATOR='+sim],tree/'tb/pp_top','build.log')
def gates():return run(['make','-j16','aecpcmd','links','matrix','reqtags','modmatrix','params','ids','figures'],tree,'gates.log')
def decode():
 if (receipts/'decode-identical.txt').exists() and (receipts/'decode-identical.txt').read_text().strip()=='True': return 0
 rc=run(['make','-j16','record','VERILATOR='+sim],tree/'tb/aecp_cmds','decode-record.log')
 if not rc:
  same=(tree/'tb/aecp_cmds/decode.json').read_bytes()==(a.source/'tb/aecp_cmds/decode.json').read_bytes()
  (receipts/'decode-identical.txt').write_text(str(same)+'\n');assert same
 return rc
with concurrent.futures.ThreadPoolExecutor(3) as pool:
 results=list(pool.map(lambda f:f(),[build,gates,decode]))
assert results==[0,0,0],results
spec=importlib.util.spec_from_file_location('mutants',tree/'tb/pp_top/notify_mutants.py');m=importlib.util.module_from_spec(spec);sys.modules['mutants']=m;spec.loader.exec_module(m)
selected=[x for x in m.MUTANTS if x.name in ['enq_dropped_configuration','configuration_compare_whole_lane','configuration_unchanged_notifies','configuration_success_reserved_dirty','configuration_refusal_notifies']]
jobs=[('golden-notify','--notify-only',None,()),('golden-dispatch','--aecp-dispatch-only',None,())]
for x in selected:jobs.append((x.name,'--notify-only',x,x.checks))
for name,check in [('scfg-range-bad-arguments','SC1'),('scfg-nsd-zero-body','SC2'),('scfg-nsd-stores','SC3'),('scfg-nsd-notifies','SC1'),('scfg-refusal-short-body','SC1')]:jobs.append((name,'--aecp-dispatch-only','patch',(check,)))
def trial(job):
 name,flag,mut,checks=job;case=scratch/name
 shutil.copytree(tree,case,ignore=shutil.ignore_patterns('obj*','__pycache__'),dirs_exist_ok=True)
 if mut=='patch':subprocess.run(['git','apply',str(tree/'tb/pp_top/aecp_dispatch_mutations'/f'{name}.patch')],cwd=case,check=True)
 elif mut is not None:
  for path,old,new in mut.edits:
   f=case/path;txt=f.read_text();assert txt.count(old)==1;f.write_text(txt.replace(old,new))
 bench=case/'tb/pp_top'
 subprocess.run([sys.executable,'-B',str(case/'hdl/aecp/ucode/gen_ucode.py'),'-o',str(bench/'ucode.hex')],check=True,stdout=subprocess.DEVNULL)
 (bench/'obj_dir').mkdir(exist_ok=True)
 rc=run([str(tree/'tb/pp_top/obj_dir/Vpp_top_sim'),flag],bench,name+'.log')
 text=(receipts/(name+'.log')).read_text();fails=[l for l in text.splitlines() if l.startswith('FAIL:')];complete='[build default,' in text
 ok=complete and ((rc==0 and not fails) if mut is None else (rc!=0 and all(any(l[5:].strip().startswith(c) for l in fails) for c in checks)))
 return dict(name=name,rc=rc,completed=complete,ok=ok,failures=fails,tally=[l for l in text.splitlines() if '[build default,' in l])
with concurrent.futures.ThreadPoolExecutor(min(16,a.jobs)) as pool:records=list(pool.map(trial,jobs))
(receipts/'results.json').write_text(json.dumps(records,indent=2)+'\n')
for r in records:print(r['name'],r['ok'],r['tally'],flush=True)
assert all(r['ok'] for r in records)
