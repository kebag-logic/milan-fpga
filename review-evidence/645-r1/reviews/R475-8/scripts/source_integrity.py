#!/usr/bin/env python3
"""Verify on-disk bytes, modes, index and initialized gitlinks against HEAD."""
import argparse,hashlib,json,os,pathlib,stat,subprocess
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("output",type=pathlib.Path);a=p.parse_args()
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],env=env)
def audit(root,ref):
 problems=[];tree=[];links=[]
 for rec in git(root,"ls-tree","-rz",ref).split(b"\0"):
  if not rec:continue
  meta,path=rec.split(b"\t",1);mode,kind,oid=meta.decode().split();name=path.decode();f=root/name
  tree.append((mode,oid,name))
  if mode=="160000":links.append((name,oid));continue
  try:
   st=f.lstat()
   if mode=="120000":data=os.fsencode(os.readlink(f));actual="120000" if stat.S_ISLNK(st.st_mode) else "wrong-kind"
   else:data=f.read_bytes();actual=("100755" if st.st_mode&0o111 else "100644") if stat.S_ISREG(st.st_mode) else "wrong-kind"
   digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
   if digest!=oid or actual!=mode:problems.append(name+": bytes/mode differ")
  except OSError as exc:problems.append(name+": "+type(exc).__name__)
 index=[]
 for rec in git(root,"ls-files","--stage","-z").split(b"\0"):
  if not rec:continue
  meta,name=rec.split(b"\t",1);mode,oid,stage=meta.decode().split();index.append((mode,oid,name.decode()))
  if stage!="0":problems.append(name.decode()+": unmerged")
 if sorted(index)!=sorted(tree):problems.append("index differs from commit tree")
 return {"head":git(root,"rev-parse",ref).decode().strip(),"tree":git(root,"rev-parse",ref+"^{tree}").decode().strip(),"files":len(tree)-len(links),"index_matches":sorted(index)==sorted(tree),"problems":problems,"gitlinks":dict(links)}
source=a.source.resolve();result=audit(source,"HEAD");result["submodules"]={}
for name,pin in result["gitlinks"].items():
 f=source/name
 if not (f/".git").is_file():
  result["submodules"][name]={"pin":pin,"initialized":False};continue
 assert pathlib.Path(git(f,"rev-parse","--show-toplevel").decode().strip()).resolve()==f
 sub=audit(f,pin);sub["actual_head"]=git(f,"rev-parse","HEAD").decode().strip()
 if sub["actual_head"]!=pin:sub["problems"].append("gitlink head mismatch")
 result["submodules"][name]=sub
required=["protocol-processor","gptp-processor","third_party/verilog-axis","third_party/lwSRP"]
result["pass"]=not result["problems"] and all(name in result["submodules"] and result["submodules"][name].get("initialized",True) and not result["submodules"][name].get("problems") for name in required)
a.output.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2));raise SystemExit(int(not result["pass"]))
