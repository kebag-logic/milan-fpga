#!/usr/bin/env python3
"""Compare actual bytes, modes and index with the exact commit and required gitlinks."""
import hashlib, os, pathlib, stat, subprocess
ROOT=pathlib.Path.cwd()
ENV=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
HEAD="33b311f5213f1fb8b47916ace9b8d872538a90e4"
REQUIRED={"protocol-processor","gptp-processor","third_party/verilog-axis"}
def git(repo,*args): return subprocess.check_output(["git", "-C",str(repo),*args],env=ENV,stderr=subprocess.DEVNULL)
def verify(repo,pin,required):
 assert git(repo,"rev-parse","HEAD").decode().strip()==pin
 entries={}
 for rec in git(repo,"ls-tree","-rz",pin).split(b"\0"):
  if not rec:continue
  meta,name=rec.split(b"\t",1);mode,kind,oid=meta.decode().split();entries[os.fsdecode(name)]=(mode,kind,oid)
 index={}
 for rec in git(repo,"ls-files","--stage","-z").split(b"\0"):
  if not rec:continue
  meta,name=rec.split(b"\t",1);mode,oid,stage=meta.decode().split();assert stage=="0"
  index[os.fsdecode(name)]=(mode,oid)
 assert index=={path:(mode,oid) for path,(mode,kind,oid) in entries.items()},"index differs"
 blobs=0
 for name,(mode,kind,oid) in entries.items():
  f=repo/name
  if kind=="commit":
   print("gitlink",name,oid)
   if name in required:
    assert f.is_dir() and not f.is_symlink()
    assert (f/".git").is_file(),"submodule is not registered"
    assert pathlib.Path(git(f,"rev-parse","--show-superproject-working-tree").decode().strip()).resolve()==repo.resolve()
    verify(f,oid,set())
   continue
  st=f.lstat()
  if mode=="120000":
   assert stat.S_ISLNK(st.st_mode),name
   b=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),name
   assert bool(st.st_mode & 0o111)==(mode=="100755"),(name,"mode")
   b=f.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
  assert actual==oid,(name,"bytes")
  blobs+=1
 print("PASS",repo.name,"head",pin,"blobs",blobs,"index entries",len(index))
verify(ROOT,HEAD,REQUIRED)
assert git(ROOT,"rev-parse","HEAD^{tree}").decode().strip()=="52b4e42eca3d57c74ede894a9452dcad0af42862"
assert not git(ROOT,"diff","--check")
print("PASS exact bytes/modes/index and all three required submodule pins")
