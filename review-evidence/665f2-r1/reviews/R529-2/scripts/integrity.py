#!/usr/bin/env python3
"""Prove raw worktree blob bytes, filesystem modes, index and required gitlinks."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
HEAD="938497af1dffd8a87edebf3ab93663914bf85e5e"
TREE="b40dfc375f080a96eb4a927e023fa6b916cbe7c1"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(where,*args):
 return subprocess.check_output(["git","--no-optional-locks","-C",str(where),*args],env=env)
def prove(where,head):
 records=git(where,"ls-tree","-rz",head).split(b"\0")
 expected=[]; errors=[]; links=[]; count=0
 for record in filter(None,records):
  meta,path=record.split(b"\t",1); mode,kind,oid=meta.split()
  expected.append(mode+b" "+oid+b" 0\t"+path+b"\0")
  file=where/os.fsdecode(path)
  if kind==b"commit":
   links.append((os.fsdecode(path),oid.decode())); continue
  try:
   s=file.lstat()
   if mode==b"120000":
    assert stat.S_ISLNK(s.st_mode)
    raw=os.fsencode(os.readlink(file))
   else:
    assert stat.S_ISREG(s.st_mode)
    assert bool(s.st_mode & 0o111)==(mode==b"100755")
    raw=file.read_bytes()
   got=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
   assert got==oid.decode()
   count+=1
  except Exception as exc:errors.append(os.fsdecode(path)+": "+type(exc).__name__)
 index=git(where,"ls-files","--stage","-z")
 if sorted(index.split(b"\0"))!=sorted(b"".join(expected).split(b"\0")):errors.append("index differs from tree")
 return {"head":git(where,"rev-parse","HEAD").decode().strip(),"expected":head,"blobs_verified":count,"index_matches":not errors,"errors":errors,"gitlinks":dict(links)}
x={"root":prove(root,HEAD),"tree":git(root,"rev-parse","HEAD^{tree}").decode().strip(),"submodules":{}}
for path in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
 pin=x["root"]["gitlinks"][path]
 result=prove(root/path,pin)
 result["registered"]=bool(git(root/path,"rev-parse","--show-superproject-working-tree").strip())
 result["own_top_level"]=Path(git(root/path,"rev-parse","--show-toplevel").decode().strip())==root/path
 x["submodules"][path]=result
x["status"]=git(root,"status","--porcelain=v1","--untracked-files=all").decode()
x["pass"]=x["tree"]==TREE and all(r["head"]==r["expected"] and not r["errors"] for r in [x["root"],*x["submodules"].values()]) and all(r["registered"] and r["own_top_level"] for r in x["submodules"].values())
print(json.dumps(x,indent=2))
sys.exit(not x["pass"])
