#!/usr/bin/env python3
"""Verify raw tracked blob bytes, executable modes, index entries and gitlinks."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
head="1e79ebdc06528edff74c0a7f530f20f99e3326a2"
tree="067514daece6faf87e9d675bd628759c7bec83fa"
def git(cwd,*args):return subprocess.check_output(["git",*args],cwd=cwd)
def verify(cwd,rev):
 assert git(cwd,"rev-parse","HEAD").decode().strip()==rev
 entries=[]; links=[]; expected={}; issues=[]
 for line in git(cwd,"ls-tree","-rz",rev).split(b"\0"):
  if not line:continue
  meta,path=line.split(b"\t",1);mode,kind,oid=meta.decode().split();name=os.fsdecode(path)
  expected[name]=(mode,oid,"0")
  if kind=="commit":links.append({"path":name,"gitlink":oid});continue
  p=cwd/name;st=p.lstat()
  data=os.fsencode(os.readlink(p)) if stat.S_ISLNK(st.st_mode) else p.read_bytes()
  actual_mode="120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode&0o111 else "100644")
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  if actual!=oid or actual_mode!=mode:issues.append(name)
  entries.append(name)
 index={}
 for line in git(cwd,"ls-files","--stage","-z").split(b"\0"):
  if not line:continue
  meta,path=line.split(b"\t",1);mode,oid,stage=meta.decode().split();index[os.fsdecode(path)]=(mode,oid,stage)
 assert not issues,(str(cwd),issues)
 assert index==expected,(str(cwd),"index differs")
 status=git(cwd,"status","--porcelain=v1","--untracked-files=all").decode()
 assert not status,(str(cwd),status)
 return {"head":rev,"tree":git(cwd,"rev-parse",rev+"^{tree}").decode().strip(),"verified_raw_blobs_and_modes":len(entries),"index_exact":True,"status_clean":True,"gitlinks":links}
result={"root":verify(root,head),"submodules":{}}
assert result["root"]["tree"]==tree
required={"protocol-processor","gptp-processor","third_party/verilog-axis"}
for link in result["root"]["gitlinks"]:
 p=root/link["path"]
 if (p/".git").exists():result["submodules"][link["path"]]=verify(p,link["gitlink"])
 else:
  assert link["path"] not in required
  result["submodules"][link["path"]]={"gitlink":link["gitlink"],"initialized":False}
assert required<=result["submodules"].keys()
(Path(__file__).resolve().parent/"tree-verification.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
