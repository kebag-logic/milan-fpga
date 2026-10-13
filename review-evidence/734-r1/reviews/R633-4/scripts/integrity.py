#!/usr/bin/env python3
"""Check bytes and modes directly against tree objects, independently of index flags."""
import hashlib,json,os,pathlib,stat,subprocess
root=pathlib.Path.cwd()
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"})
def audit(root,rev):
 rows=git(root,"ls-tree","-rz",rev).split(b"\0"); expected=[]; checked=0; links=[]
 for row in filter(None,rows):
  meta,name=row.split(b"\t",1);mode,kind,oid=meta.split();path=root/os.fsdecode(name)
  expected.append(mode+b" "+oid+b" 0\t"+name)
  if mode==b"160000":links.append((os.fsdecode(name),oid.decode()));continue
  info=path.lstat();actual=b"120000" if stat.S_ISLNK(info.st_mode) else (b"100755" if info.st_mode&0o111 else b"100644")
  data=os.fsencode(os.readlink(path)) if stat.S_ISLNK(info.st_mode) else path.read_bytes()
  got=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
  assert (actual,got)==(mode,oid),(str(path),"byte/mode mismatch")
  checked+=1
 index=git(root,"ls-files","--stage","-z").split(b"\0")
 assert sorted(filter(None,index))==sorted(expected),"index mismatch"
 return {"commit":rev,"tree":git(root,"rev-parse",rev+"^{tree}").decode().strip(),"verified_blobs":checked,"gitlinks":links}
head=git(root,"rev-parse","HEAD").decode().strip();out={"parent":audit(root,head),"submodules":{}}
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
 pin=dict(out["parent"]["gitlinks"])[name];assert (root/name/".git").is_file();assert git(root/name,"rev-parse","HEAD").decode().strip()==pin
 out["submodules"][name]=audit(root/name,pin)
out["status"]=git(root,"status","--porcelain=v1").decode();assert not out["status"]
print(json.dumps(out,indent=2))
