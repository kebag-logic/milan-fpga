#!/usr/bin/env python3
"""Verify raw working bytes, modes, index entries and required gitlinks."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
expected="2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895"
def git(root,*args):
 return subprocess.check_output(["git","--no-replace-objects","-C",str(root),*args])
def verify(root,rev):
 entries=git(root,"ls-tree","-rz",rev).split(b"\0")
 count=0; links={}; errors=[]; expected_index=[]
 for entry in filter(None,entries):
  meta,name=entry.split(b"\t",1);mode,kind,oid=meta.split();p=root/os.fsdecode(name)
  expected_index.append(mode+b" "+oid+b" 0\t"+name)
  if kind==b"commit":links[os.fsdecode(name)]=oid.decode();continue
  try:
   s=p.lstat()
   if mode==b"120000":
    assert stat.S_ISLNK(s.st_mode);data=os.fsencode(os.readlink(p))
   else:
    assert stat.S_ISREG(s.st_mode);assert bool(s.st_mode & 0o111)==(mode==b"100755");data=p.read_bytes()
   actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
   assert actual==oid
   count+=1
  except (OSError,AssertionError):errors.append(os.fsdecode(name))
 actual_index=git(root,"ls-files","--stage","-z").split(b"\0")
 assert sorted(filter(None,actual_index))==sorted(expected_index),"index differs from commit"
 assert not errors,errors
 return {"files_verified":count,"gitlinks":links,"index_matches":True,"raw_bytes_and_modes_match":True}
assert git(root,"rev-parse","HEAD").decode().strip()==expected
out={"head":expected,"tree":git(root,"rev-parse","HEAD^{tree}").decode().strip(),"parent":verify(root,expected),"submodules":{}}
for name in ["third_party/verilog-axis","protocol-processor","gptp-processor","third_party/tsn-c-stack"]:
 pin=out["parent"]["gitlinks"][name];p=root/name
 if not (p/".git").exists():out["submodules"][name]={"gitlink":pin,"checkout":"NOT INITIALIZED"};continue
 assert git(p,"rev-parse","HEAD").decode().strip()==pin
 out["submodules"][name]={"head":pin,**verify(p,pin)}
print(json.dumps(out,indent=2,sort_keys=True))
