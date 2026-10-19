#!/usr/bin/env python3
"""Verify all tracked bytes, modes, index entries and gitlinks without writing source."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(*args): return subprocess.check_output(["git",*args],cwd=root)
head=git("rev-parse","HEAD").decode().strip(); tree=git("rev-parse","HEAD^{tree}").decode().strip()
assert head=="83405d192c451e9fba0ea1fe4e051aafdbb332cc"
assert tree=="44576716500222854dc3c8271d5987abbaebcb1b"
expected={}
for record in git("ls-tree","-rz","HEAD").split(b"\0"):
 if record:
  meta,path=record.split(b"\t",1);mode,kind,oid=meta.decode().split(); expected[os.fsdecode(path)]=(mode,oid)
index={}
for record in git("ls-files","--stage","-z").split(b"\0"):
 if record:
  meta,path=record.split(b"\t",1);mode,oid,stage=meta.decode().split();assert stage=="0";index[os.fsdecode(path)]=(mode,oid)
errors=[];gitlinks=[]
for name,(mode,oid) in expected.items():
 f=root/name
 if mode=="160000":
  actual=subprocess.check_output(["git","rev-parse","HEAD"],cwd=f).decode().strip();gitlinks.append({"path":name,"expected":oid,"actual":actual})
  if actual!=oid:errors.append(name+": gitlink")
  continue
 data=os.fsencode(os.readlink(f)) if mode=="120000" else f.read_bytes()
 got=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 actual_mode="120000" if f.is_symlink() else ("100755" if f.stat().st_mode & stat.S_IXUSR else "100644")
 if got!=oid or actual_mode!=mode:errors.append(name)
assert index==expected;assert not errors
status=git("status","--porcelain=v1","--untracked-files=all").decode();assert not status
print(json.dumps({"head":head,"tree":tree,"tracked_entries_verified":len(expected),"byte_or_mode_errors":errors,"index_equals_head":True,"gitlinks":gitlinks,"status":status},indent=2))
