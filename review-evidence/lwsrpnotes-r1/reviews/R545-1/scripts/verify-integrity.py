#!/usr/bin/env python3
"""Verify exact-head working bytes, Git modes, index entries and gitlinks."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
head="ced667d8ee35929ab5f9e77a1c5396e173a693d8"
tree="52d750190ca4c8835870598900ffb751cc85a31e"
base="a4cbe41de1c80d43f26e0d348cbdb45075273a4f"
def git(*args): return subprocess.check_output(["git","-C",str(repo),*args])
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()==tree
entries={}
for row in git("ls-tree","-rz","--full-tree","HEAD").split(b"\0"):
    if not row:continue
    meta,path=row.split(b"\t",1); mode,kind,oid=meta.decode().split()
    entries[path.decode()]={"mode":mode,"kind":kind,"oid":oid}
index={}
for row in git("ls-files","--stage","-z").split(b"\0"):
    if not row:continue
    meta,path=row.split(b"\t",1); mode,oid,stage=meta.decode().split()
    assert stage=="0",(path,stage)
    index[path.decode()]={"mode":mode,"oid":oid}
assert set(entries)==set(index)
checks=[];gitlinks=[]
for path,entry in entries.items():
    assert index[path]=={"mode":entry["mode"],"oid":entry["oid"]},path
    target=repo/path
    if entry["mode"]=="160000":
        actual=subprocess.check_output(["git","-C",str(target),"rev-parse","HEAD"]).decode().strip()
        assert actual==entry["oid"],path
        gitlinks.append({"path":path,"oid":actual});continue
    st=target.lstat()
    if stat.S_ISLNK(st.st_mode):
        data=os.fsencode(os.readlink(target));mode="120000"
    else:
        assert stat.S_ISREG(st.st_mode),path
        data=target.read_bytes();mode="100755" if st.st_mode&0o111 else "100644"
    actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    assert actual==entry["oid"] and mode==entry["mode"],path
    checks.append({"path":path,"blob":actual,"mode":mode,"index_matches":True})
status=git("status","--porcelain=v1","--untracked-files=all").decode()
assert not status,status
source_trees=[git("rev-parse",ref+":src").decode().strip() for ref in [base,head]]
assert source_trees[0]==source_trees[1]
print(json.dumps({"head":head,"tree":tree,"tracked_files":checks,"required_gitlinks":gitlinks,
                 "gitlinks_note":"No gitlink entries or .gitmodules exist in this exact repository tree." if not gitlinks else "Gitlink working heads and index entries verified.",
                 "source_trees_base_and_head":source_trees,"status_porcelain":status,"result":"PASS"},indent=2))
