#!/usr/bin/env python3
"""Verify every tracked byte, file mode, index entry and submodule gitlink."""
import argparse, hashlib, json, os, pathlib, stat, subprocess
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); a=p.parse_args()
root=pathlib.Path(a.repo); packet=pathlib.Path(__file__).resolve().parents[1]
def git(*args): return subprocess.check_output(['git',*args],cwd=root)
head=git('rev-parse','HEAD').decode().strip(); tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='cb730a2f9dd7e4f60a03a38d4b47b569e68da8df'; assert tree=='f18d266c67b8b0f79341168ecdac8b4655b50b06'
entries={}
for line in git('ls-tree','-rz','HEAD').split(b'\0'):
 if line:
  meta,path=line.split(b'\t',1); mode,kind,oid=meta.decode().split(); entries[path.decode()]=(mode,kind,oid)
index={}
for line in git('ls-files','--stage','-z').split(b'\0'):
 if line:
  meta,path=line.split(b'\t',1); mode,oid,stage=meta.decode().split(); assert stage=='0'; index[path.decode()]=(mode,oid)
rows=[]; gitlinks=[]
for path,(mode,kind,oid) in entries.items():
 assert index.get(path)==(mode,oid),path
 if kind=='commit':
  gitlinks.append(dict(path=path,commit=oid)); assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root/path).decode().strip()==oid; continue
 f=root/path
 if mode=='120000': data=os.readlink(f).encode(); actual_mode='120000'
 else: data=f.read_bytes(); actual_mode='100755' if f.stat().st_mode & stat.S_IXUSR else '100644'
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert actual==oid and actual_mode==mode,path
 rows.append(dict(path=path,mode=mode,blob=oid))
assert len(index)==len(entries)
status=git('status','--porcelain=v1','--untracked-files=all').decode(); assert not status,status
r=dict(head=head,tree=tree,tracked_blob_count=len(rows),index_entries=len(index),gitlinks=gitlinks,status=status,result='PASS',tracked_blobs=rows)
(packet/'receipts/checkout-integrity.json').write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps({k:v for k,v in r.items() if k!='tracked_blobs'}))
