#!/usr/bin/env python3
"""Compare raw worktree bytes, modes, index entries and submodule pins with immutable trees."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
HEAD='ede700b00ef4d79566a6f108b11ce9bd4ad6beaa'
TREE='1efdeba1e3477de15b8f04c5615c6d58e2756e46'
env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=env)
def inventory(repo,rev):
 rows={}
 for raw in git(repo,'ls-tree','-r','-z',rev).split(b'\0'):
  if raw:
   meta,path=raw.split(b'\t',1);mode,kind,oid=meta.decode().split();rows[path.decode()]=(mode,kind,oid)
 return rows
def verify(repo,rev):
 expected=inventory(repo,rev);index={};problems=[];links={};blobs=0
 for raw in git(repo,'ls-files','--stage','-z').split(b'\0'):
  if raw:
   meta,path=raw.split(b'\t',1);mode,oid,stage=meta.decode().split()
   if stage!='0' or path.decode() in index:problems.append('unmerged/duplicate index: '+path.decode())
   index[path.decode()]=(mode,oid)
 if index!={n:(v[0],v[2]) for n,v in expected.items()}:problems.append('index differs from immutable tree')
 for name,(mode,kind,oid) in expected.items():
  path=repo/name
  if mode=='160000':links[name]=oid;continue
  try:
   st=path.lstat()
   if mode=='120000':
    assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
   else:
    assert stat.S_ISREG(st.st_mode)
    assert bool(st.st_mode&0o111)==(mode=='100755')
    data=path.read_bytes()
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   if actual!=oid:problems.append('blob mismatch: '+name)
   blobs+=1
  except (OSError,AssertionError):problems.append('file type/mode/read mismatch: '+name)
 return {'revision':rev,'entries':len(expected),'blobs_checked':blobs,'gitlinks':links,'problems':problems}
assert git(root,'rev-parse','HEAD').decode().strip()==HEAD
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
result={'head':HEAD,'tree':TREE,'root':verify(root,HEAD),'submodules':{}}
for name,pin in result['root']['gitlinks'].items():
 path=root/name
 if (path/'.git').exists():
  got=git(path,'rev-parse','HEAD').decode().strip();item=verify(path,pin);item['head_matches']=got==pin
  result['submodules'][name]=item
 else:result['submodules'][name]={'gitlink':pin,'checkout':'uninitialized; unused by focused review'}
result['status_porcelain']=git(root,'status','--porcelain=v1').decode()
result['pass']=not result['root']['problems'] and not result['status_porcelain'] and all(not x.get('problems') and x.get('head_matches',True) for x in result['submodules'].values())
print(json.dumps(result,indent=2));sys.exit(0 if result['pass'] else 1)
