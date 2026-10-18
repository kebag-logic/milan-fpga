#!/usr/bin/env python3
import hashlib,json,pathlib,re,stat,subprocess,sys
ROOT=pathlib.Path(sys.argv[1]).resolve()
def git(*a): return subprocess.check_output(["git","-C",str(ROOT),*a])
H="88cb206135c23eb86488ad110fe19cfca5f341cf"
T="946711a023752a17d1e5b0a65a6cd5e84815b6e3"
assert git("rev-parse","HEAD").decode().strip()==H
assert git("rev-parse","HEAD^{tree}").decode().strip()==T
assert not git("status","--porcelain","--untracked-files=no")
entries=git("ls-tree","-rz","HEAD").split(b"\0")
count=0; links=[]
for row in entries:
 if not row: continue
 meta,name=row.split(b"\t",1); mode,kind,oid=meta.decode().split(); p=ROOT/name.decode()
 if kind=="commit": links.append((name.decode(),oid));continue
 data=p.read_bytes() if mode!="120000" else __import__("os").readlink(p).encode()
 actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert actual==oid,(p,"bytes")
 assert (mode=="100755")==bool(p.stat().st_mode & stat.S_IXUSR),(p,"mode")
 count+=1
assert git("write-tree").decode().strip()==T
print("PASS exact HEAD/tree/index and",count,"tracked blob bytes/modes; gitlinks:",links)
def changed(a,b):return set(git("diff","--name-only",a,b).decode().splitlines())
a=changed("08ae0013","e11fb36b");b=changed("08ae0013","5addf297")
assert not a&b
for p in a: assert git("show","e11fb36b:"+p)==git("show","4e87b88:"+p),p
for p in b: assert git("show","5addf297:"+p)==git("show","4e87b88:"+p),p
assert changed("08ae0013","4e87b88")==a|b
print("PASS merge: disjoint",len(a),"issue paths and",len(b),"main paths; every result equals owning parent")
strip=lambda s:re.sub(rb"/\*.*?\*/|//[^\n]*",b"",s,flags=re.S)
for p in changed("HEAD^","HEAD"):
 if p.endswith(".sv"): assert strip(git("show","HEAD^:"+p)).split()==strip(git("show","HEAD:"+p)).split(),p
 elif p.endswith(".patch"):
  def edits(x):return [s for s in x.splitlines() if s[:1] in (b"+",b"-") and s[:3] not in (b"+++",b"---")]
  assert edits(git("show","HEAD^:"+p))==edits(git("show","HEAD:"+p)),p
  subprocess.run(["git","-C",str(ROOT),"apply","--check",p],check=True)
 else: assert p.endswith(".md"),p
print("PASS final commit: executable RTL unchanged; all 12 revised patches apply and retain identical +/- edits")
for p in ["hdl/top/protocol_processor_top.sv","hdl/srp/KL_srp_top.sv"]:
 if p.endswith("KL_srp_top.sv"):
  x=git("show","5addf297:"+p);y=git("show","HEAD:"+p)
  assert x.split(b");",1)[0]==y.split(b");",1)[0]
 else: assert git("show","5addf297:"+p)==git("show","HEAD:"+p)
print("PASS external top port/parameter contracts preserved")
