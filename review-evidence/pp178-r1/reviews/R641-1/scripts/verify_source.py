#!/usr/bin/env python3
"""Verify HEAD, tree, tracked bytes, executable modes, index, and gitlinks."""
import hashlib,json,os,pathlib,subprocess,sys
source=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parents[1]
def git(*args):return subprocess.check_output(['git',*args],cwd=source)
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='ebc3b6bcd6e2c789c1c80c9e285193628567ea33'
assert tree=='8e0a529be44ab7bef20f3418e682908c500f70a7'
expected={};bad=[];gitlinks=[]
for record in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not record:continue
 meta,path=record.split(b'\t',1);mode,kind,oid=meta.decode().split();name=os.fsdecode(path);expected[name]=(mode,oid)
 if kind=='commit':
  actual=subprocess.check_output(['git','-C',str(source/name),'rev-parse','HEAD']).decode().strip();gitlinks.append(dict(path=name,expected=oid,actual=actual));assert actual==oid
 else:
  f=source/name;data=os.fsencode(os.readlink(f)) if mode=='120000' else f.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  actualmode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
  if (actualmode,actual)!=(mode,oid):bad.append(name)
index={}
for record in git('ls-files','-sz').split(b'\0'):
 if not record:continue
 meta,path=record.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';index[os.fsdecode(path)]=(mode,oid)
assert index==expected;assert not bad
result=dict(head=head,tree=tree,tracked_entries=len(expected),byte_or_mode_mismatches=bad,index_matches_head=True,gitlinks=gitlinks,status=git('status','--porcelain=v1','--untracked-files=all').decode(),ignored=git('status','--porcelain=v1','--ignored').decode())
assert not result['status']
(packet/'receipts/source-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
