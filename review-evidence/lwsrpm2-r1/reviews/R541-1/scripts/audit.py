# SPDX-License-Identifier: Apache-2.0
"""Compare all tracked bytes, modes and index entries with the frozen head."""
import argparse, hashlib, pathlib, re, stat, subprocess, sys
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,required=True);a=p.parse_args()
root=a.source.resolve();head="86a5f74c028dedec2a0f5bc1c5a258bbd83746b9";tree="7cf49d0d499d21227764282b9d64c8de86f83758"
def git(*args):return subprocess.check_output(["git",*args],cwd=root,text=True)
entries=git("ls-tree","-r",head).splitlines();bad=[];spdx=[];privacy=[];gitlinks=[];expected=[]
for line in entries:
 metadata,name=line.split("\t",1);mode,kind,oid=metadata.split();expected.append(f"{mode} {oid} 0\t{name}")
 if mode=="160000":gitlinks.append((name,oid));continue
 file=root/name;data=file.read_bytes();actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 observed="100755" if file.stat().st_mode&stat.S_IXUSR else "100644"
 if actual!=oid or observed!=mode:bad.append(name)
 if b"SPDX-License-Identifier: Apache-2.0" not in data:spdx.append(name)
 if re.search(rb"/home/|/data/|/Users/",data,re.I):privacy.append(name)
index_ok=git("ls-files","--stage").splitlines()==expected
head_ok=git("rev-parse","HEAD").strip()==head;tree_ok=git("rev-parse","HEAD^{tree}").strip()==tree
status=git("status","--porcelain=v1","--untracked-files=all")
print(f"HEAD {head}; matches={head_ok}\nTREE {tree}; matches={tree_ok}\nTracked files: {len(entries)}\nBlob/mode mismatches: {bad}\nIndex matches: {index_ok}\nSPDX missing: {spdx}\nPrivate-path matches: {privacy}\nRequired gitlinks: {gitlinks}\nStatus: {status!r}")
sys.exit(int(bool(bad or spdx or privacy or not index_ok or not head_ok or not tree_ok or status)))
