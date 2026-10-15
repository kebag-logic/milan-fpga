#!/usr/bin/env python3
"""Compare tracked bytes, modes, index stages and required gitlinks to real commit trees."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent
head='08adb21af0a72d839ce30b6c461503dad269d4d6'; tree='e5cc5d163c974aaf1b6cb888dae9881267d787e6'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1');results=[]
def git(p,*args):return subprocess.check_output(['git',*args],cwd=p,env=env)
def verify(p,rev,label):
 entries={}
 for entry in git(p,'ls-tree','-rz',rev).split(b'\0'):
  if not entry:continue
  metadata,name=entry.split(b'\t',1);mode,kind,oid=metadata.split();entries[name]=(mode,oid)
  if kind==b'commit':continue
  path=p/os.fsdecode(name);info=path.lstat()
  if mode==b'120000':assert stat.S_ISLNK(info.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(info.st_mode) and bool(info.st_mode&0o111)==(mode==b'100755'),name
   data=path.read_bytes()
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid.decode(),name
 index={}
 for entry in git(p,'ls-files','--stage','-z').split(b'\0'):
  if not entry:continue
  metadata,name=entry.split(b'\t',1);mode,oid,stage=metadata.split();assert stage==b'0' and name not in index;index[name]=(mode,oid)
 assert index==entries,label
 results.append({'repository':label,'head':rev,'tracked_entries':len(entries),'blob_bytes_modes_index':'equal'})
 return entries
assert git(root,'rev-parse','HEAD').decode().strip()==head
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==tree
entries=verify(root,head,'superproject')
required=['protocol-processor','gptp-processor','third_party/tsn-c-stack','third_party/verilog-axis','third_party/lwSRP']
for name in required:
 mode,oid=entries[name.encode()];p=root/name
 assert mode==b'160000' and git(p,'rev-parse','HEAD').strip()==oid
 assert pathlib.Path(git(p,'rev-parse','--show-toplevel').decode().strip()).resolve()==p
 verify(p,oid.decode(),name)
runner=(root/'scripts/act_ci.py').read_bytes();assert runner==git(root,'show','84ee9ea1:scripts/act_ci.py')
result={'head':head,'tree':tree,'repositories':results,'unchanged_host_runner_sha256':hashlib.sha256(runner).hexdigest(),'delta_files':git(root,'diff','--name-only','84ee9ea1..HEAD').decode().splitlines(),'uninitialized_unused_gitlink':'external'}
(out/'checkout-integrity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
