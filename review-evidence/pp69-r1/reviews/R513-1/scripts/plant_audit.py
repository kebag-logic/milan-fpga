#!/usr/bin/env python3
"""Check every published patch and exact-text arm without running a bank."""
import argparse, importlib.util, io, json, pathlib, subprocess, sys, tarfile
sys.dont_write_bytecode=True
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1]; tree=packet/'scratch/plant-tree'; tree.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive','HEAD'],cwd=a.repo))) as tf: tf.extractall(tree,filter='data')
def module(path):
 s=importlib.util.spec_from_file_location('audit_'+path.replace('/','_'),tree/path); m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m); return m
rows=[]
for patch in sorted(tree.glob('tb/**/*.patch')):
 r=subprocess.run(['git','apply','--check',str(patch)],cwd=tree,capture_output=True,text=True)
 rows.append(dict(group='patch',name=str(patch.relative_to(tree)),ok=r.returncode==0,detail=r.stderr))
for path in ['tb/pp_top/notify_mutants.py','tb/pp_top/d3_mutants.py','tb/pp_top/acmp_mutants.py']:
 m=module(path)
 for i,arm in enumerate(m.MUTANTS):
  original={rel:(tree/rel).read_bytes() for rel,_,_ in arm.edits}
  try: refusal=m.plant(tree,arm.edits)
  finally:
   for rel,data in original.items(): (tree/rel).write_bytes(data)
  rows.append(dict(group='plant',name=f'{path}:{i}:{arm.name}',ok=not refusal,detail=refusal))
m=module('tb/acmp_talker/retry_mutants.py'); source=(tree/m.RTL).read_text()
for name in m.MUTATIONS:
 try: m.mutated_source(source,name); error=''
 except Exception as e: error=str(e)
 rows.append(dict(group='other-text',name='retry:'+name,ok=not error,detail=error))
m=module('tb/pp_top/gsi_mutants.py')
for name,path,old,new,count,check in m.mutations():
 found=(tree/path).read_text().count(old); rows.append(dict(group='other-text',name='gsi:'+name,ok=found==count,detail=f'{found}/{count} anchors'))
m=module('tb/srp_admission/mutants.py')
for name,edits,checks in m.MUTANTS:
 source=(tree/m.ADMISSION).read_text(); ok=True
 for old,new,count in edits: ok &= source.count(old)==count; source=source.replace(old,new)
 rows.append(dict(group='other-text',name='admission:'+name,ok=ok,detail=''))
source=(tree/'hdl/aecp/KL_aecp_engine.sv').read_text(); found=source.count('  assign name_wr_o = d3_nchg_w;')
rows.append(dict(group='other-text',name='name-write:decode',ok=found==1,detail=f'{found}/1 anchors'))
source=(tree/'hdl/aecp/KL_aecp_desc_mem_guard.sv').read_text(); found=source.count(' && !owed_r')
rows.append(dict(group='guard-sites',name='desc_mem_guard:no_hold',ok=found==2,detail=f'{found}/2 sites; one mutation removes both'))
summary={g:dict(total=sum(r['group']==g for r in rows),passed=sum(r['group']==g and r['ok'] for r in rows)) for g in ['patch','plant','other-text','guard-sites']}
out=packet/'receipts/plant-audit.json'; out.write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.repo,text=True).strip(),summary=summary,arms=rows),indent=2)+'\n')
print(json.dumps(summary)); print('failures', [r for r in rows if not r['ok']]); raise SystemExit(any(not r['ok'] for r in rows))
