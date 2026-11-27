#!/usr/bin/env python3
"""Prove tracked bytes, executable bits, index entries and required gitlinks without trusting status."""
import hashlib,json,os,pathlib,stat,subprocess,sys
ROOT=pathlib.Path.cwd(); OUT=pathlib.Path(__file__).resolve().parent
HEAD="0f7402ee97d347352b8c3d613033c440ee55986a"
ENV=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],env=ENV)
def verify(root,rev):
 entries=[]
 for raw in git(root,"ls-tree","-rz",rev).split(b"\0"):
  if not raw:continue
  meta,path=raw.split(b"\t",1);mode,kind,oid=meta.decode().split(); name=os.fsdecode(path)
  entries.append((mode,oid,name))
 index=[]
 for raw in git(root,"ls-files","--stage","-z").split(b"\0"):
  if not raw:continue
  meta,path=raw.split(b"\t",1);mode,oid,stage=meta.decode().split()
  assert stage=="0"
  index.append((mode,oid,os.fsdecode(path)))
 assert index==entries,"index differs from committed tree"
 count=0
 for mode,oid,name in entries:
  if mode=="160000":continue
  p=root/name;s=p.lstat()
  if mode=="120000":
   assert stat.S_ISLNK(s.st_mode),name
   data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(s.st_mode),name
   assert bool(s.st_mode&0o111)==(mode=="100755"),name
   data=p.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert actual==oid,name
  count+=1
 return entries,count
assert git(ROOT,"rev-parse","HEAD").decode().strip()==HEAD
entries,count=verify(ROOT,HEAD)
results={"head":HEAD,"tree":git(ROOT,"rev-parse","HEAD^{tree}").decode().strip(),"tracked_files":count,"bytes_modes_index":"PASS","submodules":[]}
for name in ["protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack"]:
 mode,pin,_=next(e for e in entries if e[2]==name)
 sub=ROOT/name
 assert mode=="160000" and not sub.is_symlink() and (sub/".git").is_file(),name
 actual=git(sub,"rev-parse","HEAD").decode().strip();assert actual==pin
 _,n=verify(sub,pin)
 results["submodules"].append({"path":name,"pin":pin,"tracked_files":n,"bytes_modes_index":"PASS"})
results["external"]="Not initialized; not a required local gate input."
name=sys.argv[1] if len(sys.argv)>1 else "checkout-final.json"
(OUT/name).write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results))
