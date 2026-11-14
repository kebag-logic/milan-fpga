"""Check tracked file bytes, executable bits, index entries, and required gitlinks. Argument: checkout."""
import hashlib,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
HEAD="716a8ae7979a31315a6e085959dc4dcc8b7ee022"
TREE="8e97d3d90fe0725105f3deb5822cca0841babef3"
def git(p,*args):return subprocess.check_output(["git","-C",str(p),*args])
def verify(p,expected,label):
 assert git(p,"rev-parse","HEAD").decode().strip()==expected
 entries={}
 for record in git(p,"ls-tree","-rz","HEAD").split(b"\0"):
  if not record:continue
  header,name=record.split(b"\t",1); mode,kind,oid=header.decode().split();name=os.fsdecode(name)
  entries[name]=(mode,oid)
  if kind=="commit":continue
  f=p/name;st=f.lstat()
  if mode=="120000":assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode)
   assert bool(st.st_mode & 0o111)==(mode=="100755"),(label,name,"mode")
   data=f.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert actual==oid,(label,name,"bytes")
 index={}
 for record in git(p,"ls-files","-s","-z").split(b"\0"):
  if not record:continue
  header,name=record.split(b"\t",1);mode,oid,stage=header.decode().split()
  assert stage=="0";index[os.fsdecode(name)]=(mode,oid)
 assert index==entries,(label,"index mismatch")
 print(label,"HEAD",expected,"tracked entries",len(entries),"bytes/modes/index PASS")
 return entries
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==TREE
entries=verify(root,HEAD,"candidate")
required=("gptp-processor","protocol-processor","third_party/lwSRP","third_party/tsn-c-stack","third_party/verilog-axis")
for name in required:
 mode,oid=entries[name];assert mode=="160000";verify(root/name,oid,name)
print("external gitlink",entries["external"][1],"unchanged in index/tree; intentionally uninitialized")
print("git status porcelain:",repr(git(root,"status","--porcelain=v1").decode()))
print("RESULT PASS")
