#!/usr/bin/env python3
"""Prove tracked working bytes, executable modes, index and required gitlinks."""
import hashlib,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(repo,*args): return subprocess.check_output(["git","--no-replace-objects","-C",str(repo),*args])
def records(data,tree):
 out={}
 for row in data.split(b"\0"):
  if not row: continue
  head,name=row.split(b"\t",1); mode,second,third=head.decode().split()
  assert tree or third=="0", "unmerged index"
  out[os.fsdecode(name)]=(mode,third if tree else second)
 return out
def verify(repo,rev):
 expected=records(git(repo,"ls-tree","-rz",rev),True)
 index=records(git(repo,"ls-files","--stage","-z"),False)
 assert expected==index, "index differs from tree"
 count=0
 for name,(mode,oid) in expected.items():
  if mode=="160000": continue
  p=repo/name; info=p.lstat()
  if mode=="120000":
   assert stat.S_ISLNK(info.st_mode); data=os.fsencode(os.readlink(p))
  else:
   assert stat.S_ISREG(info.st_mode),name
   assert bool(info.st_mode&0o111)==(mode=="100755"),name
   data=p.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert actual==oid,name
  count+=1
 print(repo.name,rev,"tracked file bytes/modes and index PASS",count)
 return expected
head=git(root,"rev-parse","HEAD").decode().strip()
assert head=="f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21"
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()=="90eef089759111d73b0316ded772250ee95a9735"
tree=verify(root,head)
for sub in ("gptp-processor","protocol-processor","third_party/verilog-axis","third_party/lwSRP","third_party/tsn-c-stack"):
 mode,pin=tree[sub]; assert mode=="160000"
 assert git(root/sub,"rev-parse","HEAD").decode().strip()==pin
 verify(root/sub,pin)
print("external historical dependency gitlink:",tree["external"],"checkout uninitialized; no active consumer")
print("PASS: exact head, tree, all tracked blobs/modes/index, five required submodule gitlinks and their blobs")
