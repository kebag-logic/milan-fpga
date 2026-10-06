#!/usr/bin/env python3
"""Verify every tracked blob, mode and index entry against the reviewed tree."""
import hashlib, json, os, pathlib, stat, subprocess, sys
repo, packet=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:])
head="75c4eee4589e9317aca3d07b91f94a38b4cc86af"
tree="43f1dbf62f8151c5ad158546494174fd434032c3"
def git(*args):return subprocess.check_output(["git","-C",str(repo),*args])
fail=[]; entries=[]; gitlinks=[]
for rec in git("ls-tree","-rz",head).split(b"\0"):
    if not rec: continue
    meta,rawpath=rec.split(b"\t",1);mode,kind,oid=meta.decode().split();rel=os.fsdecode(rawpath);f=repo/rel
    if mode=="160000":
        got=subprocess.check_output(["git","-C",str(f),"rev-parse","HEAD"]).decode().strip()
        gitlinks.append({"path":rel,"expected":oid,"actual":got})
        if got!=oid:fail.append(rel+": gitlink")
        continue
    st=f.lstat()
    if stat.S_ISLNK(st.st_mode): data=os.fsencode(os.readlink(f));actualmode="120000"
    else: data=f.read_bytes();actualmode="100755" if st.st_mode & 0o111 else "100644"
    got=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    if got!=oid or actualmode!=mode:fail.append(rel+": blob/mode")
    entries.append((mode,oid,rel))
index=[]
for rec in git("ls-files","--stage","-z").split(b"\0"):
    if not rec:continue
    meta,rawpath=rec.split(b"\t",1);mode,oid,stage=meta.decode().split()
    if stage!="0":fail.append(os.fsdecode(rawpath)+": nonzero index stage")
    if mode!="160000":index.append((mode,oid,os.fsdecode(rawpath)))
if entries!=index:fail.append("index entries differ from tree")
actualhead=git("rev-parse","HEAD").decode().strip();actualtree=git("rev-parse","HEAD^{tree}").decode().strip()
if actualhead!=head or actualtree!=tree:fail.append("HEAD/tree differs")
status=git("status","--porcelain=v1","--untracked-files=all").decode()
if status:fail.append("nonempty worktree status")
detached=subprocess.run(["git","-C",str(repo),"symbolic-ref","-q","HEAD"],capture_output=True).returncode==1
result={"head":actualhead,"tree":actualtree,"detached":detached,"tracked_blobs_checked":len(entries),"index_matches":entries==index,"gitlinks":gitlinks,"status":status,"failures":fail}
(packet/"receipts/checkout-integrity.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2));sys.exit(bool(fail) or not detached)
