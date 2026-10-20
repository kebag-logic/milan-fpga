#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index and public consumer gitlinks."""
import hashlib,json,os,re,stat,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SRC=Path(sys.argv[1]).resolve()
HEAD="7f56fc4d7f5102cac6dacb9c00f372d20d3b379e"
TREE="34af6de87215cc90a774757debc8af90073aaa87"
def git(*args): return subprocess.check_output(["git","-C",str(SRC),*args])
assert git("rev-parse","HEAD").decode().strip()==HEAD
assert git("rev-parse","HEAD^{tree}").decode().strip()==TREE
assert git("write-tree").decode().strip()==TREE
assert not git("status","--porcelain")
entries=git("ls-tree","-rz","HEAD").split(b"\0")
count=0;links=[]
for entry in entries:
 if not entry: continue
 meta,name=entry.split(b"\t",1); mode,kind,oid=meta.decode().split(); file=SRC/os.fsdecode(name)
 if mode=="160000": links.append(os.fsdecode(name)); continue
 data=os.readlink(file).encode() if mode=="120000" else file.read_bytes()
 actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert actual==oid,str(file)
 if mode!="120000": assert bool(file.stat().st_mode & 0o111)==(mode=="100755"),str(file)
 count+=1
assert not links
print(f"PASS HEAD {HEAD}; tree/index {TREE}; {count} tracked blob bytes and modes; clean worktree; zero processor gitlinks")
for name in ["consumer-base-tree","live-dev-tree"]:
 data=json.loads((ROOT/(name+".json")).read_text())
 assert not data.get("truncated")
 pins={x["path"]:x["sha"] for x in data["tree"] if x["mode"]=="160000"}
 print(name,json.dumps(pins,sort_keys=True))
 if name=="consumer-base-tree":
  assert len(pins)==6
  for rev,sha in [("base","cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48"),("head","cca12e3cbdbecc00eeb62d11c74dfb19d6472af0")]:
   text=(ROOT/f"public/author-r2/receipts/round2/consumers/{rev}/STATE.txt").read_text()
   for path,pin in pins.items():
    expected=sha if path=="protocol-processor" else pin
    assert re.search(r"^ "+expected+r" "+re.escape(path)+r" ",text,re.M),path
   print(f"PASS consumer {rev}: all six public gitlinks match with declared processor substitution {sha}")
print("PASS no source edits or probes performed in this round")
