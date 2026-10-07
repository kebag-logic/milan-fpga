#!/usr/bin/env python3
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
expected="351ae81f33efc1ca818c1fea21d360260ecc2587"
def git(r,*args):
 return subprocess.check_output(["git","--no-replace-objects","-C",str(r),*args])
def verify(r,head):
 assert git(r,"rev-parse","HEAD").decode().strip()==head
 tree=git(r,"ls-tree","-rz",head).split(b"\0")
 index=git(r,"ls-files","-s","-z").split(b"\0")
 ix={}
 for x in index:
  if not x:continue
  meta,path=x.split(b"\t",1);mode,oid,stage=meta.split();assert stage==b"0"
  ix[path]=(mode,oid)
 count=0;links={}
 for x in tree:
  if not x:continue
  meta,path=x.split(b"\t",1);mode,kind,oid=meta.split()
  assert ix.pop(path)==(mode,oid),str(path)
  f=r/os.fsdecode(path)
  if kind==b"commit":
   links[os.fsdecode(path)]=oid.decode();continue
  st=f.lstat()
  data=os.fsencode(os.readlink(f)) if mode==b"120000" else f.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert actual==oid.decode(),str(path)
  assert (stat.S_ISLNK(st.st_mode) if mode==b"120000" else stat.S_ISREG(st.st_mode))
  if mode!=b"120000":assert bool(st.st_mode & 0o111)==(mode==b"100755"),str(path)
  count+=1
 assert not ix
 return {"head":head,"tree":git(r,"rev-parse",head+"^{tree}").decode().strip(),"verified_blob_bytes_and_modes":count,"index_matches":True,"gitlinks":links}
report={"superproject":verify(root,expected)}
for sub in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
 report[sub]=verify(root/sub,report["superproject"]["gitlinks"][sub])
print(json.dumps(report,indent=2))
