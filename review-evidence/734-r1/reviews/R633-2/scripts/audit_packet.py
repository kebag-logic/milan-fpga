#!/usr/bin/env python3
"""Verify exact source/index bytes, selected public evidence and linked image identity."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root,packet=map(lambda p:pathlib.Path(p).resolve(),sys.argv[1:])
HEAD='33ac35b54648ef919227c5dd8b9abc97fa6bedbd'; TREE='42ffc92e382df24433ffc80333174e7d03ab4006'; BASE='a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def digest(b):return hashlib.sha256(b).hexdigest()
def entries(repo,rev):
 out={}
 for entry in git(repo,'ls-tree','-rz',rev).split(b'\0'):
  if not entry:continue
  meta,name=entry.split(b'\t',1); mode,kind,oid=meta.decode().split();out[os.fsdecode(name)]=(mode,kind,oid)
 return out

def verify_tree(repo,rev):
 tree=entries(repo,rev); index={}
 for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  meta,name=row.split(b'\t',1); mode,oid,stage=meta.decode().split();assert stage=='0'
  index[os.fsdecode(name)]=(mode,oid)
 assert index=={p:(m,o) for p,(m,k,o) in tree.items()},'index differs'
 blobs=0;links={}
 for name,(mode,kind,oid) in tree.items():
  path=repo/name
  if mode=='160000':links[name]=oid;continue
  st=path.lstat()
  if mode=='120000':assert stat.S_ISLNK(st.st_mode); data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode),(name,'not regular')
   assert bool(st.st_mode&0o111)==(mode=='100755'),(name,'mode')
   data=path.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert actual==oid,(name,'byte mismatch')
  blobs+=1
 return {'revision':rev,'tracked_blobs_verified':blobs,'index_matches_tree':True,'gitlinks':links}
assert git(root,'rev-parse','HEAD').decode().strip()==HEAD
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
result={'head':HEAD,'tree':TREE,'parent':verify_tree(root,HEAD),'required_submodules':{}}
for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
 pin=result['parent']['gitlinks'][sub]
 assert git(root/sub,'rev-parse','HEAD').decode().strip()==pin
 result['required_submodules'][sub]=verify_tree(root/sub,pin)
assert not git(root,'status','--porcelain=v1'), 'worktree not clean'
result['status']='clean'
result['unchanged_product_trees']={}
for path in ['hdl','sw','configs','syn','REQUIREMENTS.md','.gitmodules']:
 before=git(root,'rev-parse',BASE+':'+path).decode().strip(); after=git(root,'rev-parse',HEAD+':'+path).decode().strip(); assert before==after
 result['unchanged_product_trees'][path]=after
(packet/'receipts/tree-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
public=packet/'public/author-r2'; head_record=json.loads((public/'r2-head.json').read_text());assert head_record['head']==HEAD
for row in head_record['source_files']:
 data=(root/row['path']).read_bytes();assert len(data)==row['bytes'] and digest(data)==row['sha256'],row
manifest={r['file']:r for r in json.loads((packet/'public/MANIFEST.json').read_text())}
verified=[]; redacted=[]
for p in public.iterdir():
 key='author-r2/'+p.name
 if key in manifest:
  record=manifest[key]
  assert digest(p.read_bytes())==record['published_sha256'],p.name
  verified.append(p.name)
  if record['path_redacted']:redacted.append(p.name)
for p in public.glob('*.json'):
 data=json.loads(p.read_text());log=p.with_suffix('.log')
 if isinstance(data,dict) and 'sha256' in data and log.exists():
  record=manifest['author-r2/'+log.name]
  assert data['sha256']==record['original_sha256'],p.name
  if not record['path_redacted']:
   assert digest(log.read_bytes())==data['sha256'],p.name
   assert len(log.read_bytes())==data['bytes'],p.name
assert digest((packet/'scripts/probe_scope.py').read_bytes())==digest((packet/'public/reviews/R632-1/scripts/probe_scope.py').read_bytes())
images=[];image_root=packet/'scratch/linked-images-final/images'
for row in json.loads((public/'r2-image-hashes.json').read_text()):
 shape=row['shape'];a=(image_root/'base'/shape/'ctrl_app.elf').read_bytes();b=(image_root/'head'/shape/'ctrl_app.elf').read_bytes();assert a==b
 images.append({'shape':shape,'bytes':len(b),'base_sha256':digest(a),'head_sha256':digest(b),'equals_published_author_hash':digest(b)==row['after_sha256']})
(packet/'receipts/linked-image-hashes.json').write_text(json.dumps(images,indent=2)+'\n')
audit={'evidence_commit':'872d08f828de11c7e3b4919afd3d75cce3c2f999','selected_manifest_receipts_verified':verified,'publisher_redaction_records':redacted,'source_bindings_verified':len(head_record['source_files']),'prior_probe_unmodified':True,'five_elf_pairs_identical':True}
(packet/'receipts/public-evidence-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({'source':result,'evidence':audit,'images':images},indent=2))
