#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index entries and required submodule gitlinks."""
import hashlib,os,pathlib,stat,subprocess,sys
R=pathlib.Path(sys.argv[1]).resolve()
os.environ["GIT_NO_REPLACE_OBJECTS"]="1"
def git(r,*a):return subprocess.check_output(["git","-C",str(r),*a])
def verify(r,rev):
 rows=git(r,"ls-tree","-rz",rev).split(b"\0"); expected=[]; count=0; subs=[]
 for row in rows:
  if not row:continue
  info,name=row.split(b"\t",1);mode,typ,oid=info.decode().split();path=r/os.fsdecode(name)
  expected.append((mode,oid,os.fsdecode(name)))
  if typ=="commit":subs.append((os.fsdecode(name),oid));continue
  s=path.lstat();assert not stat.S_ISDIR(s.st_mode),path
  data=os.fsencode(os.readlink(path)) if mode=="120000" else path.read_bytes()
  assert (mode=="120000")==stat.S_ISLNK(s.st_mode),path
  if mode!="120000":assert bool(s.st_mode & 0o111)==(mode=="100755"),path
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest();assert actual==oid,path
  count+=1
 index=[]
 for row in git(r,"ls-files","-s","-z").split(b"\0"):
  if row:
   info,name=row.split(b"\t",1);mode,oid,stage=info.decode().split();assert stage=="0"
   index.append((mode,oid,os.fsdecode(name)))
 assert sorted(index)==sorted(expected),"index entries"
 flags=git(r,"ls-files","-v","-z").split(b"\0")
 assert not any(x and (chr(x[0]).islower() or x[0]==ord("S")) for x in flags),"hidden flags"
 print(str(r.relative_to(R)) or ".",rev,"blobs",count,"bytes/modes/index PASS")
 return subs
head=git(R,"rev-parse","HEAD").decode().strip();tree=git(R,"rev-parse","HEAD^{tree}").decode().strip()
assert head=="64e55a59e09339114926c2600056c3ad8b33b9b4"
assert tree=="ee8f0eb03b6f360cd507678ef029970ec43afc95"
print("head",head,"tree",tree)
subs=dict(verify(R,head))
for name in ["protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack","third_party/lwSRP"]:
 r=R/name;assert r.is_dir() and not r.is_symlink()
 assert (r/".git").is_file(),"must be initialized registered submodule"
 assert git(r,"rev-parse","HEAD").decode().strip()==subs[name]
 verify(r,subs[name])
assert git(R,"status","--porcelain")==b""
print("Required submodule gitlinks verified; original clone clean. external is unused and uninitialized.")
