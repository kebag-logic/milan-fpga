#!/usr/bin/env python3
"""Prove tracked bytes, Git modes, index and initialized gitlinks against HEAD."""
import hashlib, os, pathlib, stat, subprocess, sys
repo=pathlib.Path(sys.argv[1]).resolve()
expected="af2c4d7a4a1930aba712792a7facd8e9cb88e7c7"
def git(root,*args):
 return subprocess.check_output(["git","-C",str(root),*args])
assert git(repo,"rev-parse","HEAD").decode().strip()==expected
assert git(repo,"rev-parse","HEAD^{tree}").decode().strip()=="63cae1575a884c869dd92698c8d4a9bb685f6aba"
required={"gptp-processor","protocol-processor","third_party/lwSRP","third_party/tsn-c-stack","third_party/verilog-axis"}
def verify(root,label):
 entries={}
 for item in git(root,"ls-tree","-rz","HEAD").split(b"\0"):
  if not item:continue
  meta,name=item.split(b"\t",1);mode,kind,oid=meta.split()
  entries[name]=(mode,kind,oid)
 index={}
 for item in git(root,"ls-files","--stage","-z").split(b"\0"):
  if not item:continue
  meta,name=item.split(b"\t",1);mode,oid,stage=meta.split()
  assert stage==b"0",(label,name,stage)
  index[name]=(mode,oid)
 assert index=={n:(v[0],v[2]) for n,v in entries.items()},label+" index differs"
 for item in git(root,"ls-files","-v","-z").split(b"\0"):
  if item:assert item[:1]==b"H",(label,item)
 blobs=0
 for name,(mode,kind,oid) in entries.items():
  path=root/os.fsdecode(name)
  if kind==b"commit":
   if label=="superproject" and os.fsdecode(name) in required:
    assert (path/".git").exists() and not path.is_symlink()
    actual=git(path,"rev-parse","HEAD").strip()
    assert actual==oid,(name,actual,oid)
    assert git(path,"rev-parse","--show-superproject-working-tree").decode().strip()==str(repo)
    verify(path,os.fsdecode(name))
   elif label=="superproject":
    assert os.fsdecode(name)=="external" and not (path/".git").exists()
    print("external: gitlink "+oid.decode()+" unchanged; uninitialized.")
   continue
  info=path.lstat()
  if mode==b"120000":
   assert stat.S_ISLNK(info.st_mode)
   data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(info.st_mode)
   assert mode==(b"100755" if info.st_mode&0o111 else b"100644"),(label,name,"mode")
   data=path.read_bytes()
  digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
  assert digest==oid,(label,name,"bytes")
  blobs+=1
 assert not git(root,"diff","--raw","HEAD"),label+" diff"
 assert not git(root,"status","--porcelain","--untracked-files=all"),label+" status"
 print(f"{label}: {len(entries)} tree/index entries, {blobs} raw blobs and modes identical; no hidden/sparse flags; clean.")
verify(repo,"superproject")
print("HEAD "+expected)
print("TREE 63cae1575a884c869dd92698c8d4a9bb685f6aba")
print("Integrity: PASS")

