#!/usr/bin/env python3
"""Check exact tracked bytes, modes, index entries, HEAD and gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(*a): return subprocess.check_output(["git","-C",str(root),*a])
head="ad670a71b4d2f38f59672d51d8309d59ffed0808"
tree="224aadfa2ffc348ad3123bd4580b573a7d97c098"
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()==tree
assert subprocess.run(["git","-C",str(root),"symbolic-ref","-q","HEAD"],stdout=subprocess.DEVNULL).returncode==1,"not detached"
entries=[]; links=[]
for line in git("ls-tree","-rz", "HEAD").split(b"\0"):
 if not line: continue
 meta,path=line.split(b"\t",1); mode,kind,oid=meta.decode().split(); name=os.fsdecode(path)
 entries.append((mode,oid,"0",name))
 if mode=="160000":
  links.append((name,oid)); assert subprocess.check_output(["git","-C",str(root/name),"rev-parse","HEAD"]).decode().strip()==oid
  continue
 f=root/name
 b=os.fsencode(os.readlink(f)) if mode=="120000" else f.read_bytes()
 actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
 assert actual==oid,(name,"blob mismatch")
 actualmode="120000" if f.is_symlink() else ("100755" if f.stat().st_mode&stat.S_IXUSR else "100644")
 assert actualmode==mode,(name,"mode mismatch")
index=[]
for line in git("ls-files","--stage","-z").split(b"\0"):
 if not line: continue
 meta,path=line.split(b"\t",1); mode,oid,stage=meta.decode().split();index.append((mode,oid,stage,os.fsdecode(path)))
assert entries==index,"index differs from exact head"
assert not git("status","--porcelain","--untracked-files=no")
print(json.dumps({"head":head,"tree":tree,"tracked_entries":len(entries),"gitlinks":links,"bytes_modes_index":"PASS","tracked_status":"clean"},indent=2))
