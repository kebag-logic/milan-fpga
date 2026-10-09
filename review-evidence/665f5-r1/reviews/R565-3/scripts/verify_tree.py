#!/usr/bin/env python3
"""Verify raw tracked bytes, executable modes, index entries and required gitlinks."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve(); expected=sys.argv[2]
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(root,*args):
 return subprocess.check_output(["git","-C",str(root),*args],env=env)
def blob(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def check(path,revision):
 assert git(path,"rev-parse","HEAD").decode().strip()==revision
 tree=git(path,"rev-parse",revision+"^{tree}").decode().strip()
 assert git(path,"write-tree").decode().strip()==tree
 expected_entries=[]; links=[]; rows=[]
 for row in git(path,"ls-tree","-rz",revision).split(b"\0"):
  if not row:continue
  meta,name=row.split(b"\t",1);mode,kind,oid=meta.decode().split();name=os.fsdecode(name)
  expected_entries.append((mode,oid,name))
  if mode=="160000":links.append((name,oid));continue
  target=path/name; st=target.lstat()
  if mode=="120000":
   assert stat.S_ISLNK(st.st_mode),(name,"not a symlink")
   data=os.fsencode(os.readlink(target))
  else:
   assert stat.S_ISREG(st.st_mode),(name,"not regular")
   assert bool(st.st_mode&0o111)==(mode=="100755"),(name,"mode differs")
   data=target.read_bytes()
  assert blob(data)==oid,(name,"tracked raw bytes differ")
  rows.append(f"{mode} {oid} {name}\n")
 entries=[]
 for row in git(path,"ls-files","--stage","-z").split(b"\0"):
  if not row:continue
  meta,name=row.split(b"\t",1);mode,oid,stage=meta.decode().split()
  assert stage=="0"
  entries.append((mode,oid,os.fsdecode(name)))
 assert entries==expected_entries,"index entries differ from commit"
 return {"head":revision,"tree":tree,"files":len(rows),"raw_bytes_modes_index":"PASS", "inventory_sha256":hashlib.sha256("".join(rows).encode()).hexdigest()},links
result,links=check(root,expected)
required={"protocol-processor","gptp-processor","third_party/verilog-axis","third_party/lwSRP"}
result["submodules"]=[]
for name,pin in links:
 if name not in required:continue
 path=root/name
 assert not path.is_symlink() and (path/".git").is_file(),(name,"not registered submodule")
 assert pathlib.Path(git(path,"rev-parse","--show-toplevel").decode().strip()).resolve()==path
 item,_=check(path,pin);item["path"]=name
 result["submodules"].append(item)
assert {x["path"] for x in result["submodules"]}==required
result["status"]=git(root,"status","--porcelain=v2").decode()
assert not result["status"],"worktree is dirty"
print(json.dumps(result,indent=2))
