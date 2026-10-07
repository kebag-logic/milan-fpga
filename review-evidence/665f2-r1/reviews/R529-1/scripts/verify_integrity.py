#!/usr/bin/env python3
"""Prove raw tracked bytes, modes, index entries and required submodule pins."""
import argparse,hashlib,json,os,pathlib,stat,subprocess
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("output",type=pathlib.Path);a=p.parse_args()
root=a.source.resolve();env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
expected="1a5d70faba6a9b01aab6bb868c12e4c7023e0c70"
def git(r,*args):return subprocess.check_output(["git","-C",str(r),*args],env=env)
def check(r,revision):
 entries={};issues=[];files=0
 for record in git(r,"ls-tree","-rz",revision).split(b"\0"):
  if not record:continue
  meta,name=record.split(b"\t",1);mode,kind,oid=meta.decode().split();path=r/os.fsdecode(name);entries[name]=(mode,oid)
  if kind=="commit":continue
  try:
   st=path.lstat();link=stat.S_ISLNK(st.st_mode)
   actual="120000" if link else "100755" if st.st_mode&0o111 else "100644"
   if not link and not stat.S_ISREG(st.st_mode):raise ValueError("not a regular file")
   data=os.fsencode(os.readlink(path)) if link else path.read_bytes()
   digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
   if actual!=mode or digest!=oid:issues.append(os.fsdecode(name)+": bytes or mode mismatch")
   files+=1
  except Exception as ex:issues.append(os.fsdecode(name)+": "+str(ex))
 index={}
 for record in git(r,"ls-files","--stage","-z").split(b"\0"):
  if not record:continue
  meta,name=record.split(b"\t",1);mode,oid,stage=meta.decode().split()
  if stage!="0" or name in index:issues.append("unmerged/duplicate index: "+os.fsdecode(name))
  index[name]=(mode,oid)
 if entries!=index:issues.append("index differs from committed entries")
 flags=[os.fsdecode(x) for x in git(r,"ls-files","-v","-z").split(b"\0") if x and x[:1]!=b"H"]
 if flags:issues.append("index visibility flags: "+repr(flags))
 return {"revision":revision,"files_hashed":files,"entries":len(entries),"issues":issues}
head=git(root,"rev-parse","HEAD").decode().strip();assert head==expected
result={"head":head,"tree":git(root,"rev-parse","HEAD^{tree}").decode().strip(),"superproject":check(root,head),"submodules":{}}
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
 pin=git(root,"ls-tree","HEAD",name).decode().split()[2];sub=root/name
 measured=git(sub,"rev-parse","HEAD").decode().strip();row=check(sub,pin)
 if measured!=pin:row["issues"].append("HEAD differs from gitlink")
 if not (sub/".git").is_file():row["issues"].append("missing registered gitfile")
 row["head"]=measured;result["submodules"][name]=row
result["status_porcelain"]=git(root,"status","--porcelain").decode()
result["pass"]=not result["status_porcelain"] and not result["superproject"]["issues"] and all(not x["issues"] for x in result["submodules"].values())
a.output.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
raise SystemExit(0 if result["pass"] else 1)
