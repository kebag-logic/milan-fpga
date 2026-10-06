#!/usr/bin/env python3
import argparse,hashlib,importlib.util,io,json,pathlib,re,subprocess,tarfile
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();r=a.repo.resolve();p=a.packet.resolve();out={}
def git(*args):return subprocess.check_output(['git',*args],cwd=r)
base='86a7b0c57831c15e9cd8b42d64cc4a9843f4e726';head='cd9825c947cf67b735d26cc1c42541ccd9d7f637'
for ref in [base,head]:
 tree=p/'scratch'/('audit-'+ref[:8]);tree.mkdir(exist_ok=True)
 with tarfile.open(fileobj=io.BytesIO(git('archive',ref))) as tf:tf.extractall(tree,filter='data')
 patches=sorted(tree.glob('tb/**/*.patch'));records=[]
 for patch in patches:
  x=subprocess.run(['git','apply','--check',str(patch)],cwd=tree,capture_output=True,text=True)
  records.append({'path':str(patch.relative_to(tree)),'rc':x.returncode,'output':x.stderr})
 out[ref]={'patches':records,'count':len(records),'refused':sum(x['rc']!=0 for x in records)}
 spec=importlib.util.spec_from_file_location('notify_audit',tree/'tb/pp_top/notify_mutants.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 arms=[]
 for mut in m.MUTANTS:
  buffers={};errors=[]
  for rel,old,new in mut.edits:
   text=buffers.get(rel,(tree/rel).read_text());count=text.count(old)
   if count!=1:errors.append({'path':rel,'occurrences':count})
   buffers[rel]=text.replace(old,new,1)
  arms.append({'name':mut.name,'errors':errors})
 out[ref]['notify_exact_text']=arms
 out[ref]['notify_refused']=sum(bool(x['errors']) for x in arms)
files=['hdl/top/protocol_processor_top.sv','hdl/packet_engine/KL_pp_tx_arbiter.sv']
out['interfaces']={}
for f in files:
 old=git('show',base+':'+f).decode();new=(r/f).read_text()
 # No difference through the end of the module's port declaration.
 oh=old[:old.index('\n);')+3] if '\n);' in old else old[:old.index('\n  //')]
 nh=new[:new.index('\n);')+3] if '\n);' in new else new[:new.index('\n  //')]
 out['interfaces'][f]={'equal':oh==nh,'sha256':hashlib.sha256(nh.encode()).hexdigest()}
# Every changed HDL line is absent from the pre-change bench mutation inputs.
diff=git('diff',base,head,'--',*files).decode();removed=[l[1:] for l in diff.splitlines() if l.startswith('-') and not l.startswith('---') and l[1:].strip() not in ['','end']]
btree=p/'scratch'/('audit-'+base[:8]);targets=[f for f in (btree/'tb').rglob('*') if f.is_file() and (f.suffix in ['.patch','.py'] or f.name=='README.md')]
out['prechange_line_audit']=[{'text':l,'hits':[str(f.relative_to(btree)) for f in targets if l in f.read_text(errors='replace')]} for l in removed]
# Verify public publication manifest against downloaded bytes.
public=p/'receipts/public-evidence';out['public_hashes']=[{'file':i['file'],'matches':hashlib.sha256((public/i['file']).read_bytes()).hexdigest()==i['published_sha256']} for i in json.loads((public/'MANIFEST.json').read_text())]
(p/'receipts/static-audit.json').write_text(json.dumps(out,indent=2)+'\n')
for ref in [base,head]:print(ref,'patches',out[ref]['count'],'refused',out[ref]['refused'],'notify arms',len(out[ref]['notify_exact_text']),'refused',out[ref]['notify_refused'])
print('module interfaces',out['interfaces']);print('prechange line hits',sum(bool(x['hits']) for x in out['prechange_line_audit']));print('public hash failures',sum(not x['matches'] for x in out['public_hashes']))
assert all(not out[ref]['refused'] and not out[ref]['notify_refused'] for ref in [base,head]);assert all(x['equal'] for x in out['interfaces'].values());assert all(x['matches'] for x in out['public_hashes'])
