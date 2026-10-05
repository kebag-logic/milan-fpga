#!/usr/bin/env python3
"""Compare tracked bytes, modes and index to an exact commit, including required gitlinks."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
HEAD="fb4953bd61b0f6ca61ab067081e766fe37f96076"
REQUIRED=("protocol-processor","gptp-processor","third_party/verilog-axis")
def git(root,*args):
 return subprocess.check_output(["git","-C",str(root),*args])
def audit(root,ref,label):
 assert git(root,"rev-parse","HEAD").decode().strip()==ref, label+" head"
 entries=[]
 for rec in git(root,"ls-tree","-rz","--full-tree",ref).split(b"\0"):
  if not rec: continue
  meta,path=rec.split(b"\t",1); mode,kind,oid=meta.split(); entries.append((mode,oid,path))
 expected=b"".join(m+b" "+h+b" 0\t"+p+b"\0" for m,h,p in entries)
 actual=git(root,"ls-files","--stage","-z")
 assert expected==actual,label+" index mismatch"
 count=0
 for mode,oid,path in entries:
  p=root/os.fsdecode(path)
  if mode==b"160000": continue
  st=p.lstat()
  if mode==b"120000":
   assert stat.S_ISLNK(st.st_mode)
   data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(st.st_mode),str(path)
   assert bool(st.st_mode&0o111)==(mode==b"100755"),str(path)
   data=p.read_bytes()
  digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert digest==oid.decode(),str(path)
  count+=1
 result={"population":label,"head":ref,"tree":git(root,"rev-parse",ref+"^{tree}").decode().strip(),"tracked_blobs_verified":count,"index_sha256":hashlib.sha256(actual).hexdigest(),"status":"PASS"}
 print(json.dumps(result,sort_keys=True))
 return entries
root=Path(sys.argv[1]).resolve()
entries=audit(root,HEAD,"parent")
for name in REQUIRED:
 pin=next(h.decode() for m,h,p in entries if p.decode()==name and m==b"160000")
 assert (root/name/".git").is_file(),name+" not registered submodule"
 assert git(root/name,"rev-parse","--show-superproject-working-tree").strip(),name+" missing superproject"
 audit(root/name,pin,name)
