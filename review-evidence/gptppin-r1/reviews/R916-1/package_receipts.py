#!/usr/bin/env python3
"""Normalize host paths in receipts and list publishable root files.
Usage: python3 package_receipts.py OUTPUT
Scratch trees are never listed. REPORT.md is included in the hash manifest.
"""
import hashlib,pathlib,re,sys
out=pathlib.Path(sys.argv[1]).resolve()
for file in out.glob("*.log"):
 text=file.read_text()
 text=re.sub(r"/home/[^\s'\"]+","<external-install>",text)
 text=text.replace(str(out),"<packet>")
 text=text.replace("$VALIDATION_TOOLS/pinned-verilator-5.050/verilator","<simulator>")
 file.write_text(text)
files=sorted(p for p in out.iterdir() if p.is_file() and p.name!="MANIFEST.sha256")
allowed={".md",".py",".log",".rc",".patch",".json",".txt"}
assert all(p.suffix in allowed for p in files)
report=(out/"REPORT.md").read_text()
assert report.splitlines()[0]=="[R916] NEGATIVE - exact head bbfdb6746d585e490508783dc8a88c79fbab02c0"
assert "SKELETON" not in report
assert report.splitlines()[-1]=="R916-1 FINISHED"
for file in files:
 assert re.search(rb"/home/[A-Za-z0-9]",file.read_bytes()) is None,file.name
manifest="".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.name+"\n" for p in files)
(out/"MANIFEST.sha256").write_text(manifest)
print("PASS publication manifest:",len(files),"files; scratch excluded")
