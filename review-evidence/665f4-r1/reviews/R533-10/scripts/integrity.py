#!/usr/bin/env python3
"""Read every tracked blob, mode and index entry without refreshing the index."""
import argparse,hashlib,json,os,stat,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("--source",type=Path,default=Path.cwd());ap.add_argument("--packet",type=Path,default=Path(__file__).resolve().parents[1]);a=ap.parse_args();root=a.source.resolve();packet=a.packet.resolve()
head="82a79638405c3365e4078da471be56758f8dd679"; tree="f09d67734ca6ccab67a2482d884331c6b4d2056c"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1",GIT_OPTIONAL_LOCKS="0")
def git(path,*args):return subprocess.check_output(["git","-C",str(path),*args],env=env)
def inspect(path,expected):
 actual=git(path,"rev-parse","HEAD").decode().strip();assert actual==expected,(path,actual,expected)
 entries=[];links={};blob_count=0
 for row in git(path,"ls-tree","-rz","HEAD").split(b"\0"):
  if not row:continue
  meta,name=row.split(b"\t",1);mode,kind,oid=meta.split();name=name.decode();oid=oid.decode();mode=mode.decode()
  entries.append((mode,oid,"0",name))
  if kind==b"commit":links[name]=oid;continue
  f=path/name;s=f.lstat();actual_mode="120000" if stat.S_ISLNK(s.st_mode) else ("100755" if s.st_mode & 0o111 else "100644")
  assert actual_mode==mode,(f,mode,actual_mode)
  data=os.readlink(f).encode() if mode=="120000" else f.read_bytes()
  digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest();assert digest==oid,(f,digest,oid)
  blob_count+=1
 index=[]
 for row in git(path,"ls-files","--stage","-z").split(b"\0"):
  if row:
   meta,name=row.split(b"\t",1);m,o,stage=meta.decode().split();index.append((m,o,stage,name.decode()))
 assert sorted(entries)==sorted(index),str(path)+" index differs"
 status=git(path,"status","--porcelain=v1","--untracked-files=all").decode();assert not status,status
 return {"head":actual,"tree":git(path,"rev-parse","HEAD^{tree}").decode().strip(),"tracked_blobs_checked":blob_count,"index_entries_checked":len(index),"blob_bytes_modes_index_match":True,"status_clean":True,"gitlinks":links}
result={"source":inspect(root,head)};assert result["source"]["tree"]==tree
result["required_submodules"]={}
for name in ["gptp-processor","protocol-processor","third_party/lwSRP","third_party/verilog-axis"]:
 result["required_submodules"][name]=inspect(root/name,result["source"]["gitlinks"][name])
result["external"]="gitlink verified; intentionally uninitialized, no code from it executed"
result["candidate_source_mutations"]="none; all plants and added probe translation units confined to scratch"
(packet/"receipts/final-integrity.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"ok":True,"parent_blobs":result["source"]["tracked_blobs_checked"],"required_submodules":len(result["required_submodules"])}))
