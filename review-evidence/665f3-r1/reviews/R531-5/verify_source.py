#!/usr/bin/env python3
"""Verify raw tracked bytes, executable modes, index and required gitlinks."""
import argparse, hashlib, json, os, stat, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("repo",type=Path);a=ap.parse_args()
os.environ["GIT_NO_REPLACE_OBJECTS"]="1"
def git(repo,*args):
 return subprocess.check_output(["git","-C",str(repo),*args])
def check(repo,expected):
 assert git(repo,"rev-parse","HEAD").decode().strip()==expected
 entries=git(repo,"ls-tree","-rz",expected).split(b"\0")
 index=git(repo,"ls-files","--stage","-z").split(b"\0")
 want=[];count=0;links=[]
 for e in entries:
  if not e:continue
  meta,name=e.split(b"\t",1);mode,kind,oid=meta.split();path=repo/os.fsdecode(name)
  want.append(mode+b" "+oid+b" 0\t"+name)
  if kind==b"commit":links.append((os.fsdecode(name),oid.decode()));continue
  st=path.lstat()
  if mode==b"120000":
   assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode),str(path)
   assert bool(st.st_mode & 0o111)==(mode==b"100755"),str(path)
   data=path.read_bytes()
  raw=b"blob "+str(len(data)).encode()+b"\0"+data
  assert hashlib.sha1(raw).hexdigest()==oid.decode(),str(path)
  count+=1
 assert sorted(x for x in index if x)==sorted(want),"index differs from tree"
 return {"head":expected,"tree":git(repo,"rev-parse",expected+"^{tree}").decode().strip(),"blobs_verified":count,"gitlinks":links}
repo=a.repo.resolve();head="13e715136b0b7c8d9763e0b730d9709f2c9f5932"
result={"parent":check(repo,head),"submodules":{}}
for name,pin in result["parent"]["gitlinks"]:
 if name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
  assert (repo/name/".git").is_file(),"required registered submodule absent"
  result["submodules"][name]=check(repo/name,pin)
result["status"]="PASS"
print(json.dumps(result,indent=2))
