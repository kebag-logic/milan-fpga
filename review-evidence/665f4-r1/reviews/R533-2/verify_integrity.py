#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, stage-zero index and exact gitlinks."""
import argparse, hashlib, json, os, stat, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);a=p.parse_args()
root=a.source.resolve();packet=Path(__file__).resolve().parent
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1",GIT_OPTIONAL_LOCKS="0")
def git(where,*argv):return subprocess.check_output(["git","-C",str(where),*argv],env=env)
head="42a0371affceb2a07a734449d706be01fa5abc9a"
assert git(root,"rev-parse","HEAD").decode().strip()==head
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()=="ab9bd75e4d779adcc76aa958f696f6259ed72bb7"
def check(where,commit,label):
 assert git(where,"rev-parse","HEAD").decode().strip()==commit
 assert Path(git(where,"rev-parse","--show-toplevel").decode().strip()).resolve()==where
 raw=git(where,"ls-tree","-rz",commit);expected={};count=0;links={}
 for line in raw.split(b"\0"):
  if not line:continue
  info,name=line.split(b"\t",1);mode,kind,oid=info.split();expected[name]=(mode,oid)
  path=where/os.fsdecode(name)
  if kind==b"commit":links[os.fsdecode(name)]=oid.decode();continue
  st=path.lstat()
  if mode==b"120000":
   assert stat.S_ISLNK(st.st_mode),(label,name,"not a symlink")
   content=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode),(label,name,"not a regular file")
   assert bool(st.st_mode&0o111)==(mode==b"100755"),(label,name,"mode mismatch")
   content=path.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest().encode()
  assert actual==oid,(label,name,"blob mismatch")
  count+=1
 staged={}
 for line in git(where,"ls-files","--stage","-z").split(b"\0"):
  if not line:continue
  info,name=line.split(b"\t",1);mode,oid,stage=info.split()
  assert stage==b"0",(label,name,"unmerged")
  assert name not in staged
  staged[name]=(mode,oid)
 assert staged==expected,(label,"index differs from head")
 flags=git(where,"ls-files","-v","-z").split(b"\0")
 assert all(not f or (not f[:1].islower() and f[:1]!=b"S") for f in flags),(label,"hidden index flag")
 untracked=git(where,"ls-files","--others","--exclude-standard","-z").split(b"\0")
 ignored=git(where,"ls-files","--others","--ignored","--exclude-standard","-z").split(b"\0")
 return {"repository":label,"head":commit,"tree":git(where,"rev-parse",commit+"^{tree}").decode().strip(),
  "blobs_verified":count,"index_entries":len(staged),"gitlinks":links,
  "tree_listing_sha256":hashlib.sha256(raw).hexdigest(),"raw_bytes_modes_index":"PASS",
  "untracked":[os.fsdecode(n) for n in untracked if n],"ignored":[os.fsdecode(n) for n in ignored if n]}
results=[check(root,head,"parent")]
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis","third_party/lwSRP"):
 results.append(check(root/name,results[0]["gitlinks"][name],name))
assert all(not r["untracked"] and not r["ignored"] for r in results),"generated files remain"
(packet/"receipts/final-integrity.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
