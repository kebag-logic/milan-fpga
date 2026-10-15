#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index entries, and initialized gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent
expected='6918d4f9bee7081a71f94d9090d01c557085658a';expected_tree='cf35c3b9acfa5215f285a867f39fb583d84f01cc'
def git(path,*args):return subprocess.check_output(['git','--no-replace-objects','-C',str(path),*args])
def check(path,head):
 actual=git(path,'rev-parse','HEAD').decode().strip();assert actual==head
 entries=git(path,'ls-tree','-rz',head).split(b'\0');indexed={}
 for item in git(path,'ls-files','--stage','-z').split(b'\0'):
  if not item:continue
  meta,name=item.split(b'\t',1);mode,oid,stage=meta.split();assert stage==b'0';indexed[name]=(mode,oid)
 expected_index={};failures=[];submodules=[];blobs=0
 for item in entries:
  if not item:continue
  meta,name=item.split(b'\t',1);mode,kind,oid=meta.split();expected_index[name]=(mode,oid);f=path/os.fsdecode(name)
  if kind==b'commit':
   initialized=(f/'.git').exists()
   submodules.append({'path':os.fsdecode(name),'expected':oid.decode(),'initialized':initialized,
    'actual':git(f,'rev-parse','HEAD').decode().strip() if initialized else None})
   continue
  try:
   data=os.fsencode(os.readlink(f)) if mode==b'120000' else f.read_bytes()
   observed=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   st=f.lstat();kind_ok=stat.S_ISLNK(st.st_mode) if mode==b'120000' else stat.S_ISREG(st.st_mode)
   mode_ok=mode==b'120000' or bool(st.st_mode&0o111)==(mode==b'100755')
   if observed!=oid or not kind_ok or not mode_ok:failures.append(os.fsdecode(name))
  except OSError: failures.append(os.fsdecode(name))
  blobs+=1
 assert expected_index==indexed,'index differs from HEAD'
 assert not failures,failures
 for sub in submodules:
  if sub['initialized']:assert sub['actual']==sub['expected'],sub
 return {'head':actual,'tree':git(path,'rev-parse','HEAD^{tree}').decode().strip(),'tracked_blobs_verified':blobs,'index_matches':True,'byte_mode_failures':failures,'gitlinks':submodules}
result=check(root,expected);assert result['tree']==expected_tree
result['initialized_submodules']={s['path']:check(root/s['path'],s['expected']) for s in result['gitlinks'] if s['initialized']}
result['unchanged_workflows']=subprocess.run(['git','-C',str(root),'diff','--quiet','fa7347fc',expected,'--','.github/workflows']).returncode==0
result['status_porcelain']=git(root,'status','--porcelain').decode();assert not result['status_porcelain'];assert result['unchanged_workflows']
(out/'restore-check.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result['tracked_blobs_verified'],'parent blobs, index, modes and required gitlinks verified')
