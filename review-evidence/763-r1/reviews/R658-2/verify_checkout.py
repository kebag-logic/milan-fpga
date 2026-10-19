#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index and submodule pins: CHECKOUT PACKET."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root,packet=map(pathlib.Path,sys.argv[1:]);root=root.resolve()
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}
def git(path,*args):return subprocess.check_output(["git","-C",str(path),*args],env=env)
def check(path,rev):
 assert git(path,"rev-parse","HEAD").decode().strip()==rev
 entries={}
 for row in git(path,"ls-tree","-rz",rev).split(b"\0"):
  if not row:continue
  spec,name=row.split(b"\t",1);mode,kind,oid=spec.decode().split();entries[os.fsdecode(name)]=(mode,kind,oid)
 idx={}
 for row in git(path,"ls-files","--stage","-z").split(b"\0"):
  if not row:continue
  spec,name=row.split(b"\t",1);mode,oid,stage=spec.decode().split();assert stage=="0"
  idx[os.fsdecode(name)]=(mode,oid)
 assert idx=={n:(m,o) for n,(m,k,o) in entries.items()}
 blobs=0; links={}
 for name,(mode,kind,oid) in entries.items():
  f=path/name
  if mode=="160000":links[name]=oid;continue
  st=f.lstat()
  if mode=="120000":assert stat.S_ISLNK(st.st_mode);b=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),name
   assert bool(st.st_mode & 0o111)==(mode=="100755"),name
   b=f.read_bytes()
  assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==oid,name
  blobs+=1
 return {"head":rev,"tracked_blobs_verified":blobs,"index":"matches tree","gitlinks":links}
head="07c6c72fce79e705bcf28a70071497d0ce7040e4"
result={"parent":check(root,head),"submodules":{}}
for n in ["protocol-processor","gptp-processor","third_party/verilog-axis","third_party/lwSRP","third_party/tsn-c-stack"]:
 p=root/n;assert (p/".git").is_file(),n
 assert pathlib.Path(git(p,"rev-parse","--show-superproject-working-tree").decode().strip()).resolve()==root
 result["submodules"][n]=check(p,result["parent"]["gitlinks"][n])
assert not git(root,"status","--porcelain=v1","--untracked-files=all")
result["status"]="PASS: raw bytes, file kinds, executable modes, indexes, required registered gitlinks and clean checkout"
(packet/"receipts/checkout-integrity.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
