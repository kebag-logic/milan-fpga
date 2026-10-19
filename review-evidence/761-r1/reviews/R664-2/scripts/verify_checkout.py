#!/usr/bin/env python3
import hashlib,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
expected="eef90b4238b6c19b679b44adc6f09362809be153"
tree="ba15df1ef198a7d86150b4e33726fe0a4a10f589"
def git(repo,*args):return subprocess.check_output(["git","-C",str(repo),*args])
def verify(repo,label):
 entries={}
 for entry in git(repo,"ls-tree","-rz","--full-tree","HEAD").split(b"\0"):
  if not entry:continue
  meta,name=entry.split(b"\t",1);mode,kind,oid=meta.split();entries[name]=(mode,oid)
 index={}
 for entry in git(repo,"ls-files","--stage","-z").split(b"\0"):
  if not entry:continue
  meta,name=entry.split(b"\t",1);mode,oid,stage=meta.split();assert stage==b"0";index[name]=(mode,oid)
 assert index==entries,(label,"index differs from HEAD tree")
 count=0
 for name,(mode,oid) in entries.items():
  if mode==b"160000":continue
  f=repo/os.fsdecode(name); st=f.lstat()
  if mode==b"120000": assert stat.S_ISLNK(st.st_mode); data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(st.st_mode),(label,name,"file kind")
   actual=b"100755" if st.st_mode & 0o111 else b"100644";assert actual==mode,(label,name,"mode")
   data=f.read_bytes()
  digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
  assert digest==oid,(label,name,"raw blob mismatch")
  count+=1
 print(label,":",count,"tracked blob bytes/modes and complete index equal HEAD")
 return entries
assert git(root,"rev-parse","HEAD").decode().strip()==expected
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()==tree
print("head",expected);print("tree",tree)
entries=verify(root,"reviewed parent")
for sub in ("protocol-processor","gptp-processor","third_party/verilog-axis","third_party/tsn-c-stack"):
 mode,oid=entries[sub.encode()];assert mode==b"160000"
 assert git(root/sub,"rev-parse","HEAD").strip()==oid,(sub,"gitlink mismatch")
 print("gitlink",sub,oid.decode());verify(root/sub,sub)
print("PASS exact tracked bytes, modes, index and all four required submodule gitlinks")
