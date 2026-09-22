import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(); output=Path(sys.argv[2])
os.environ["GIT_NO_REPLACE_OBJECTS"]="1"
def git(path,*args): return subprocess.check_output(["rtk","proxy","git","-C",str(path),*args])
def inspect(path,expected=None):
 head=git(path,"rev-parse","HEAD").decode().strip()
 if expected: assert head==expected,(path,head,expected)
 records=git(path,"ls-tree","-rz","HEAD").split(b"\0")
 expected_index=[]; files=[]; subs=[]
 for row in records:
  if not row: continue
  info,name=row.split(b"\t",1); mode,kind,oid=info.decode().split(); rel=os.fsdecode(name); f=path/rel
  expected_index.append(f"{mode} {oid} 0\t".encode()+name+b"\0")
  if kind=="commit":
   if (f/".git").exists(): subs.append(dict(path=rel,expected=oid,population=inspect(f,oid)))
   else:
    assert not f.exists() or not any(f.iterdir()),str(f)
    subs.append(dict(path=rel,expected=oid,population="uninitialized"))
   continue
  s=f.lstat(); symlink=stat.S_ISLNK(s.st_mode)
  if mode=="120000": assert symlink; data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(s.st_mode),(rel,"kind")
   assert bool(s.st_mode&0o111)==(mode=="100755"),(rel,"mode")
   data=f.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert actual==oid,(rel,"blob",actual,oid)
  files.append(dict(path=rel,mode=mode,blob=oid))
 index=git(path,"ls-files","--stage","-z")
 assert index==b"".join(expected_index),(str(path),"index mismatch")
 flags=git(path,"ls-files","-v","-z").split(b"\0")
 assert all(not x or x[:1]==b"H" for x in flags),(str(path),"index flags")
 return dict(head=head,tree=git(path,"rev-parse","HEAD^{tree}").decode().strip(),files=files,submodules=subs,index_sha256=hashlib.sha256(index).hexdigest(),status=git(path,"status","--porcelain=v2").decode())
r=inspect(root,"1496558d82cf35fc98dda0e781b2a1be643c301a");output.write_text(json.dumps(r,indent=2)+"\n"); print(json.dumps(dict(head=r["head"],tree=r["tree"],files=len(r["files"]),submodules=[(s["path"],len(s["population"]["files"]) if isinstance(s["population"],dict) else s["population"]) for s in r["submodules"]],status=r["status"])))
