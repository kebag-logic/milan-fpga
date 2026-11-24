#!/usr/bin/env python3
"""Redact local execution paths and manifest the publishable review packet."""
import hashlib,pathlib,re,shutil,sys
p=pathlib.Path(sys.argv[1]).resolve();repo=pathlib.Path(sys.argv[2]).resolve()
raw=p/"scratch/raw-receipts";raw.mkdir(parents=True,exist_ok=True)
for f in sorted(p.glob("*.log")):
 if not (raw/f.name).exists(): shutil.copy2(f,raw/f.name)
 s=f.read_text()
 s=s.replace(str(p),"<packet>").replace(str(repo),"<review-clone>")
 s=re.sub(r"/home/[^\s\x22\x27]+","<compiler-root>",s)
 f.write_text(s)
files=[f for f in p.rglob("*") if f.is_file() and "scratch" not in f.relative_to(p).parts and f.name!="MANIFEST.sha256"]
with (p/"MANIFEST.sha256").open("w") as manifest:
 for f in sorted(files): manifest.write(hashlib.sha256(f.read_bytes()).hexdigest()+"  "+f.relative_to(p).as_posix()+"\n")
print("Manifest written:",len(files),"publishable files; scratch excluded")
