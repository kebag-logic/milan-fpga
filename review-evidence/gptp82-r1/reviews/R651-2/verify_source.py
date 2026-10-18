#!/usr/bin/env python3
"""Verify every tracked byte, mode, index entry and gitlink without changing source."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
P=Path(__file__).resolve().parent
R=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def git(*args):return subprocess.check_output(["rtk","proxy","git",*args],cwd=R)
rows=[]; bad=[]; links={}
for ent in git("ls-tree","-rz","HEAD").split(b"\0"):
 if not ent:continue
 meta,path=ent.split(b"\t"); mode,kind,sha=meta.decode().split(); name=os.fsdecode(path); f=R/name
 if kind=="commit":links[name]=sha;continue
 data=os.fsencode(os.readlink(f)) if mode=="120000" else f.read_bytes()
 actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 actualmode="120000" if f.is_symlink() else "100755" if f.stat().st_mode&0o111 else "100644"
 ok=actual==sha and actualmode==mode
 rows.append({"path":name,"blob":sha,"mode":mode,"bytes_and_mode_match":ok})
 if not ok:bad.append(name)
head=git("rev-parse","HEAD").decode().strip(); tree=git("rev-parse","HEAD^{tree}").decode().strip()
index=git("write-tree").decode().strip()
result={"head":head,"tree":tree,"index_tree":index,"index_matches_head_tree":index==tree,"tracked_files":len(rows),"mismatches":bad,"gitlinks":links,"status":git("status","--short","--untracked-files=all").decode(),"tracked":rows}
(P/"source-integrity.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="tracked"},indent=2))
assert head=="8f3c376d1e07d2f1417889ae2ac590c71b8cb910" and tree=="359e2e2518117b70fd1efd4287ecf2888a61d102" and index==tree and not bad and not links
